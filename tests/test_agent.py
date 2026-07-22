import subprocess
from pathlib import Path

import pytest

from src.wiki_agent import (
    Config,
    Git,
    Researcher,
    StateDB,
    Vault,
    choose_candidate,
    commit_and_push,
    find_similar_page,
    process_lock,
    resolve_target_for_duplicates,
    review_is_blocking,
    run_once,
    strip_markdown_fence,
    unescape_literal_newlines,
    validate_action,
)


def test_vault_rejects_escape(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "vault")
    with pytest.raises(ValueError):
        vault.safe("../outside.md")


def test_empty_vault_gets_creation_candidate(tmp_path: Path) -> None:
    candidate = choose_candidate(Vault(tmp_path / "vault"))
    assert candidate["action"] == "create_page"


def test_action_target_is_confined(tmp_path: Path) -> None:
    config = Config(tmp_path / "vault")
    validate_action({"action": "create_page", "target": "note.md"}, config)
    with pytest.raises(ValueError):
        validate_action({"action": "create_page", "target": "../../secret"}, config)


def test_structure_action_lets_llm_choose_target(tmp_path: Path) -> None:
    validate_action({"action": "create_structure", "reason": "connect concepts"}, Config(tmp_path / "vault"))


def test_vault_snapshot_contains_content_and_links(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "vault")
    vault.write("notes/alpha.md", "# Alpha\n\nSee [[Beta]].")
    snapshot = vault.snapshot()
    assert snapshot[0]["path"] == "notes\\alpha.md" or snapshot[0]["path"] == "notes/alpha.md"
    assert snapshot[0]["links"] == ["Beta"]
    assert "Alpha" in snapshot[0]["excerpt"]


def test_fetch_page_rejects_private_urls() -> None:
    with pytest.raises(ValueError):
        Researcher().fetch_page("http://localhost:11434/api/tags")


def test_review_warnings_are_not_blocking() -> None:
    assert not review_is_blocking({"approved": False, "issues": ["translation consistency"]})
    assert review_is_blocking({"approved": False, "issues": ["missing sources"]})
    assert review_is_blocking({"approved": False, "issues": [{"type": "factual_error"}]})


def test_process_lock_prevents_concurrent_runs(tmp_path: Path) -> None:
    lock_path = tmp_path / ".agent-run.lock"
    with process_lock(lock_path) as first:
        assert first
        with process_lock(lock_path) as second:
            assert not second
    assert not lock_path.exists()


def test_unescape_literal_newlines_fixes_double_escaped_content() -> None:
    broken = "---\\ntype: knowledge\\n---\\n\\n# Title\\n\\n## 概要\\n本文"
    fixed = unescape_literal_newlines(broken)
    assert "\\n" not in fixed
    assert fixed.startswith("---\ntype: knowledge\n---\n\n# Title")


def test_unescape_literal_newlines_leaves_real_newlines_untouched() -> None:
    already_fine = "---\ntype: knowledge\n---\n\n# Title\n"
    assert unescape_literal_newlines(already_fine) == already_fine


def test_review_with_typed_blocking_issue_is_blocking() -> None:
    review = {
        "approved": False,
        "issues": [
            {"type": "blocking", "description": "ページの内容が浅すぎます。"},
            {"type": "warning", "description": "表現の統一が必要です。"},
        ],
    }
    assert review_is_blocking(review)


def test_review_with_only_typed_warnings_is_not_blocking() -> None:
    review = {
        "approved": False,
        "issues": [{"type": "warning", "description": "表現の統一が必要です。"}],
    }
    assert not review_is_blocking(review)


def test_strip_markdown_fence_unwraps_whole_page() -> None:
    fenced = "```markdown\n---\ntitle: Home\n---\n\n# Home\n本文\n```"
    assert strip_markdown_fence(fenced) == "---\ntitle: Home\n---\n\n# Home\n本文"


def test_strip_markdown_fence_leaves_unfenced_content_untouched() -> None:
    plain = "---\ntitle: Home\n---\n\n# Home\n本文"
    assert strip_markdown_fence(plain) == plain


def test_strip_markdown_fence_handles_missing_closing_fence() -> None:
    unterminated = "```markdown\n---\ntitle: Home\n---\n\n# Home\n本文"
    assert strip_markdown_fence(unterminated) == "---\ntitle: Home\n---\n\n# Home\n本文"


def test_strip_markdown_fence_discards_stray_text_after_closing_fence() -> None:
    trailing_noise = (
        "```markdown\n---\ntitle: Home\n---\n\n# Home\n本文\n```\n"
        "- [Unrelated link](https://example.com)\n"
        "- [Another stray link](https://example.org)"
    )
    assert strip_markdown_fence(trailing_noise) == "---\ntitle: Home\n---\n\n# Home\n本文"


def test_config_rejects_unknown_mode(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        Config(tmp_path / "vault", mode="autonomous_full").validate()


def test_config_rejects_bad_ollama_url(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        Config(tmp_path / "vault", ollama_url="localhost:11434").validate()


def test_config_rejects_empty_model(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        Config(tmp_path / "vault", model="  ").validate()


def test_config_rejects_non_positive_limits(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        Config(tmp_path / "vault", max_searches=0).validate()


def test_config_accepts_valid_settings(tmp_path: Path) -> None:
    Config(tmp_path / "vault").validate()


def test_find_similar_page_matches_exact_normalized_title(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "vault")
    vault.write("10_Knowledge/Ollama の モデル管理.md", "# body")
    match = find_similar_page(vault, "Ollamaのモデル管理")
    assert match is not None
    assert match.stem == "Ollama の モデル管理"


def test_find_similar_page_matches_substring_title(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "vault")
    vault.write("10_Knowledge/自律Wiki構築AIの検索方針.md", "# body")
    match = find_similar_page(vault, "自律Wiki構築AI")
    assert match is not None


def test_find_similar_page_returns_none_for_unrelated_titles(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "vault")
    vault.write("10_Knowledge/Ollamaのモデル管理.md", "# body")
    assert find_similar_page(vault, "破滅的忘却について") is None


def test_git_is_repo_detects_non_repo_directory(tmp_path: Path) -> None:
    plain_dir = tmp_path / "not-a-repo"
    plain_dir.mkdir()
    assert not Git(plain_dir).is_repo()


def test_git_is_repo_detects_real_repo(tmp_path: Path) -> None:
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init"], cwd=repo_dir, check=True, capture_output=True)
    assert Git(repo_dir).is_repo()


def _init_repo_with_remote(tmp_path: Path) -> tuple[Path, Path]:
    remote_dir = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", str(remote_dir)], check=True, capture_output=True)
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    subprocess.run(["git", "init", str(repo_dir)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo_dir), "symbolic-ref", "HEAD", "refs/heads/main"], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "config", "user.name", "Test"], check=True)
    subprocess.run(["git", "-C", str(repo_dir), "remote", "add", "origin", str(remote_dir)], check=True)
    return repo_dir, remote_dir


def test_git_push_sends_commits_to_remote(tmp_path: Path) -> None:
    repo_dir, remote_dir = _init_repo_with_remote(tmp_path)
    (repo_dir / "note.md").write_text("# Note", encoding="utf-8")
    git = Git(repo_dir)
    git.commit("wiki: add note")
    assert git.push() is True
    remote_log = subprocess.run(
        ["git", "--git-dir", str(remote_dir), "log", "--oneline", "main"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert "wiki: add note" in remote_log


def test_commit_and_push_noop_when_auto_commit_disabled(tmp_path: Path) -> None:
    repo_dir, _ = _init_repo_with_remote(tmp_path)
    vault = Vault(repo_dir)
    vault.write("note.md", "# Note")
    config = Config(tmp_path / "unused-vault", git_enabled=True, auto_commit=False)
    assert commit_and_push(vault, config, "wiki: test") == "skipped"
    assert Git(repo_dir).status() != ""


def test_commit_and_push_noop_when_not_a_repo(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "plain_vault")
    vault.write("note.md", "# Note")
    config = Config(tmp_path / "unused-vault", git_enabled=True, auto_commit=True, auto_push=True)
    assert commit_and_push(vault, config, "wiki: test") == "skipped"


def test_commit_and_push_commits_without_pushing_by_default(tmp_path: Path) -> None:
    repo_dir, remote_dir = _init_repo_with_remote(tmp_path)
    vault = Vault(repo_dir)
    vault.write("note.md", "# Note")
    config = Config(tmp_path / "unused-vault", git_enabled=True, auto_commit=True, auto_push=False)
    assert commit_and_push(vault, config, "wiki: test commit") == "committed"
    log = subprocess.run(
        ["git", "-C", str(repo_dir), "log", "--oneline"], capture_output=True, text=True, check=True
    ).stdout
    assert "wiki: test commit" in log
    remote_log = subprocess.run(
        ["git", "--git-dir", str(remote_dir), "log", "--oneline", "--all"],
        capture_output=True,
        text=True,
    ).stdout
    assert "wiki: test commit" not in remote_log


def test_commit_and_push_pushes_when_auto_push_enabled(tmp_path: Path) -> None:
    repo_dir, remote_dir = _init_repo_with_remote(tmp_path)
    vault = Vault(repo_dir)
    vault.write("note.md", "# Note")
    config = Config(tmp_path / "unused-vault", git_enabled=True, auto_commit=True, auto_push=True)
    assert commit_and_push(vault, config, "wiki: test push") == "pushed"
    remote_log = subprocess.run(
        ["git", "--git-dir", str(remote_dir), "log", "--oneline", "main"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert "wiki: test push" in remote_log


def _clone(remote_dir: Path, target_dir: Path) -> Path:
    subprocess.run(["git", "clone", str(remote_dir), str(target_dir)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(target_dir), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(target_dir), "config", "user.name", "Test"], check=True)
    subprocess.run(
        ["git", "-C", str(target_dir), "checkout", "-B", "main", "origin/main"],
        check=True,
        capture_output=True,
    )
    return target_dir


def test_git_push_rebases_and_retries_on_non_conflicting_race(tmp_path: Path) -> None:
    repo_dir, remote_dir = _init_repo_with_remote(tmp_path)
    (repo_dir / "shared.md").write_text("# Shared", encoding="utf-8")
    git = Git(repo_dir)
    git.commit("wiki: initial")
    assert git.push() is True

    other_dir = _clone(remote_dir, tmp_path / "other")
    (other_dir / "from-other.md").write_text("# Other", encoding="utf-8")
    Git(other_dir).commit("wiki: from other process")
    assert Git(other_dir).push() is True

    (repo_dir / "from-repo.md").write_text("# Mine", encoding="utf-8")
    git.commit("wiki: from this process")
    assert git.push() is True

    remote_log = subprocess.run(
        ["git", "--git-dir", str(remote_dir), "log", "--oneline", "main"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    assert "wiki: from other process" in remote_log
    assert "wiki: from this process" in remote_log


def test_commit_and_push_returns_push_failed_on_unresolvable_conflict(tmp_path: Path) -> None:
    repo_dir, remote_dir = _init_repo_with_remote(tmp_path)
    (repo_dir / "shared.md").write_text("# Original", encoding="utf-8")
    git = Git(repo_dir)
    git.commit("wiki: initial")
    assert git.push() is True

    other_dir = _clone(remote_dir, tmp_path / "other")
    (other_dir / "shared.md").write_text("# Changed by other process", encoding="utf-8")
    Git(other_dir).commit("wiki: conflicting change from other process")
    assert Git(other_dir).push() is True

    (repo_dir / "shared.md").write_text("# Changed by this process", encoding="utf-8")
    vault = Vault(repo_dir)
    config = Config(tmp_path / "unused-vault", git_enabled=True, auto_commit=True, auto_push=True)
    assert commit_and_push(vault, config, "wiki: conflicting change from this process") == "push_failed"

    log = subprocess.run(
        ["git", "-C", str(repo_dir), "log", "--oneline"], capture_output=True, text=True, check=True
    ).stdout
    assert "wiki: conflicting change from this process" in log


def test_record_reflection_inserts_row(tmp_path: Path) -> None:
    db = StateDB(tmp_path / "state.sqlite3")
    db.record_reflection("run-1", "review rejected: missing sources", "出典が不足していた。")

    rows = db.db.execute("SELECT run_id, problem, lesson, proposed_rule FROM reflections").fetchall()
    assert rows == [("run-1", "review rejected: missing sources", "出典が不足していた。", None)]


def test_stale_pages_returns_pages_older_than_threshold(tmp_path: Path) -> None:
    import os
    import time

    vault = Vault(tmp_path / "vault")
    old_page = vault.write("old.md", "# Old")
    fresh_page = vault.write("fresh.md", "# Fresh")
    old_time = time.time() - 40 * 86400
    os.utime(old_page, (old_time, old_time))

    db = StateDB(tmp_path / "state.sqlite3")
    db.sync_pages(vault)

    stale = db.stale_pages(days=30)
    assert stale == ["old.md"]
    assert str(fresh_page.relative_to(vault.root)) not in stale


def test_resolve_target_for_duplicates_redirects_to_similar_existing_page(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "vault")
    vault.write("10_Knowledge/自律Wiki構築AI.md", "# body")
    resolved = resolve_target_for_duplicates(vault, Path("10_Knowledge/自律Wiki構築AIの概要.md"))
    assert resolved == vault.safe("10_Knowledge/自律Wiki構築AI.md")


def test_resolve_target_for_duplicates_keeps_new_target_when_unrelated(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "vault")
    vault.write("10_Knowledge/自律Wiki構築AI.md", "# body")
    target = Path("10_Knowledge/破滅的忘却について.md")
    assert resolve_target_for_duplicates(vault, target) == target


def test_task_queue_round_trip(tmp_path: Path) -> None:
    db = StateDB(tmp_path / "state.sqlite3")
    assert db.next_pending_task() is None

    db.enqueue_task("create_page", "10_Knowledge/new.md")
    task = db.next_pending_task()
    assert task is not None
    assert task["task_type"] == "create_page"
    assert task["target_page"] == "10_Knowledge/new.md"

    db.complete_task(task["task_id"])
    assert db.next_pending_task() is None


def test_run_once_prefers_queued_task_over_smallest_page(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "vault")
    vault.write("small.md", "# Small")
    config = Config(tmp_path / "vault", mode="manual")

    db = StateDB(vault.root / ".agent-state.sqlite3")
    db.enqueue_task("improve_page", "small.md")

    result = run_once(config)
    assert result["result"] == "proposal"
    assert result["action"]["target"] == "small.md"
    assert "task_id" in result["action"]


def test_status_summary_reports_recent_runs_and_counts(tmp_path: Path) -> None:
    db = StateDB(tmp_path / "state.sqlite3")
    db.db.execute(
        "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?)",
        ("run-1", "qwen3:8b", "2026-01-01T00:00:00+00:00", "2026-01-01T00:01:00+00:00", "success", 2, None),
    )
    db.db.execute(
        "INSERT INTO runs VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            "run-2",
            "qwen3:8b",
            "2026-01-02T00:00:00+00:00",
            "2026-01-02T00:01:00+00:00",
            "review_rejected",
            1,
            "missing sources",
        ),
    )
    db.db.commit()
    db.record_reflection("run-2", "missing sources", "出典が不足していた。")

    summary = db.status_summary()

    assert summary["last_run_at"] == "2026-01-02T00:00:00+00:00"
    assert summary["recent_runs"][0]["run_id"] == "run-2"
    assert summary["result_counts"] == {"success": 1, "review_rejected": 1}
    assert summary["reflection_count"] == 1
    assert summary["stale_page_count"] == 0


def test_choose_candidate_prefers_stale_page_when_db_given(tmp_path: Path) -> None:
    import os
    import time

    vault = Vault(tmp_path / "vault")
    vault.write("small.md", "# Small")
    old_page = vault.write("old.md", "# This one has been sitting untouched for a long time")
    old_time = time.time() - 40 * 86400
    os.utime(old_page, (old_time, old_time))

    db = StateDB(tmp_path / "state.sqlite3")
    db.sync_pages(vault)

    candidate = choose_candidate(vault, db, stale_days=30)
    assert candidate["action"] == "improve_page"
    assert candidate["target"] == "old.md"
