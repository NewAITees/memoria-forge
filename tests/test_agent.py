import subprocess
from pathlib import Path

import pytest

from src.wiki_agent import (
    Config,
    Git,
    LMStudio,
    Researcher,
    StateDB,
    Vault,
    choose_candidate,
    commit_and_push,
    create_client,
    find_similar_page,
    normalize_new_page_target,
    plan_rss_action,
    process_lock,
    resolve_target_for_duplicates,
    review_is_blocking,
    run_once,
    safe_new_page_target,
    strip_markdown_fence,
    unescape_literal_newlines,
    validate_action,
)
from src.rss_collector import RSSCollector, RSSEntry, load_rss_sources


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


def test_lmstudio_provider_uses_lmstudio_client(tmp_path: Path) -> None:
    config = Config(tmp_path / "vault", provider="lmstudio", ollama_url="http://localhost:1234")
    config.validate()
    assert isinstance(create_client(config), LMStudio)


def test_config_rejects_unknown_provider(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="provider"):
        Config(tmp_path / "vault", provider="unknown").validate()


def test_normalize_new_page_target_adds_or_repairs_markdown_suffix() -> None:
    from pathlib import Path

    assert normalize_new_page_target(Path("note")) == Path("note.md")
    assert normalize_new_page_target(Path("note.txt")) == Path("note.md")
    assert normalize_new_page_target(Path("note.md")) == Path("note.md")


@pytest.mark.parametrize(
    "proposed",
    [
        "../../etc/passwd",
        "../secret",
        "C:/Windows/System32/evil",
        "/etc/hosts",
        "..",
        "破滅的忘却",
    ],
)
def test_safe_new_page_target_never_escapes_the_vault(tmp_path: Path, proposed: str) -> None:
    vault = Vault(tmp_path / "vault")
    safe = safe_new_page_target(Path(proposed))
    # The sanitized target must be a Markdown path the vault accepts without raising.
    assert safe.suffix == ".md"
    resolved = vault.safe(safe)
    assert vault.root in resolved.parents


def test_safe_new_page_target_files_bare_title_under_knowledge_dir() -> None:
    assert safe_new_page_target(Path("破滅的忘却")) == Path("10_Knowledge/破滅的忘却.md")
    # A title that already carries a directory keeps it.
    assert safe_new_page_target(Path("20_Concepts/RAG")) == Path("20_Concepts/RAG.md")


class _FakeClient:
    """Minimal stand-in for Ollama/LMStudio used to drive run_once offline."""

    def __init__(self, pages: list[dict[str, object]]) -> None:
        self._pages = pages

    def plan(self, snapshot: object, stale: object = None) -> dict[str, object]:
        return {"action": "expand_knowledge", "reason": "add missing knowledge"}

    def expand(self, snapshot: object, max_new_pages: int) -> dict[str, object]:
        return {"pages": self._pages}

    def write(
        self, title: str, reason: str, sources: object, existing: str = "", feedback: str = ""
    ) -> str:
        return f"---\ntype: knowledge\nstatus: draft\n---\n\n# {title}\n\n## 概要\n\n{reason}\n"

    def review(self, content: str) -> dict[str, object]:
        return {"approved": True, "issues": []}


def test_run_once_does_not_crash_on_vault_escaping_llm_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import src.wiki_agent as wiki_agent

    vault = Vault(tmp_path / "vault")
    vault.write("10_Knowledge/seed.md", "# seed")
    config = Config(tmp_path / "vault", mode="autonomous_safe")

    fake = _FakeClient([{"target": "../../etc/passwd", "reason": "r", "search_queries": []}])
    monkeypatch.setattr(wiki_agent, "create_client", lambda _config: fake)
    monkeypatch.setattr(Researcher, "search", lambda self, query, count=3: [])

    result = run_once(config)

    # Previously this raised ValueError("path escapes vault") and killed the run.
    assert result["result"] == "expanded"
    new_pages = [Vault(config.vault_path).safe(p) for p in result["new_pages"]]
    assert all(page.exists() for page in new_pages)
    assert all(Vault(config.vault_path).root in page.parents for page in new_pages)


def test_run_once_salvages_poisoned_queue_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import src.wiki_agent as wiki_agent

    vault = Vault(tmp_path / "vault")
    vault.write("10_Knowledge/seed.md", "# seed")
    config = Config(tmp_path / "vault", mode="autonomous_safe")
    db = StateDB(vault.root / ".agent-state.sqlite3")
    # A raw, vault-escaping target left in the queue by an older run.
    db.enqueue_task("create_page", "/Knowledge/Retrieval_Experiments.md")

    fake = _FakeClient([])
    monkeypatch.setattr(wiki_agent, "create_client", lambda _config: fake)
    monkeypatch.setattr(Researcher, "search", lambda self, query, count=3: [])

    result = run_once(config)

    # Previously this looped forever on plan_rejected and stalled the scheduler.
    assert result["result"] == "success"
    assert db.next_pending_task() is None
    created = Vault(config.vault_path).safe(result["action"]["target"])
    assert created.exists()
    assert Vault(config.vault_path).root in created.parents


def test_run_once_normalizes_deferred_queue_targets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import src.wiki_agent as wiki_agent

    vault = Vault(tmp_path / "vault")
    vault.write("10_Knowledge/seed.md", "# seed")
    config = Config(tmp_path / "vault", mode="autonomous_safe", max_new_pages=1)
    # The second proposal is deferred (over max_new_pages) and carries a bad target.
    fake = _FakeClient(
        [
            {"target": "10_Knowledge/first.md", "reason": "r", "search_queries": []},
            {"target": "/Knowledge/second.md", "reason": "r", "search_queries": []},
        ]
    )
    monkeypatch.setattr(wiki_agent, "create_client", lambda _config: fake)
    monkeypatch.setattr(Researcher, "search", lambda self, query, count=3: [])

    run_once(config)

    task = StateDB(vault.root / ".agent-state.sqlite3").next_pending_task()
    assert task is not None
    assert not task["target_page"].startswith("/")
    # The queued target must be one the vault accepts without raising.
    Vault(config.vault_path).safe(task["target_page"])


def test_config_rejects_empty_model(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        Config(tmp_path / "vault", model="  ").validate()


def test_config_rejects_non_positive_limits(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        Config(tmp_path / "vault", max_searches=0).validate()


def test_config_accepts_valid_settings(tmp_path: Path) -> None:
    Config(tmp_path / "vault").validate()


def test_config_accepts_disabled_timeout(tmp_path: Path) -> None:
    Config(tmp_path / "vault", timeout_seconds=None).validate()


def test_config_rejects_non_positive_timeout(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        Config(tmp_path / "vault", timeout_seconds=0).validate()


def test_disabled_timeout_loads_and_reaches_client(tmp_path: Path) -> None:
    config_file = tmp_path / "config.json"
    config_file.write_text(
        '{"vault_path": "./vault", "ollama": '
        '{"base_url": "http://localhost:11434", "timeout_seconds": null}}',
        encoding="utf-8",
    )
    config = Config.load(config_file)
    assert config.timeout_seconds is None
    assert create_client(config).timeout is None


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


SAMPLE_FEED = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
<title>Test Feed</title>
<item><title>AI breakthrough</title><link>https://example.com/a</link>
<description>summary a</description></item>
<item><title>Robotics news</title><link>https://example.com/b</link>
<description>summary b</description></item>
</channel></rss>"""


def test_rss_collector_parses_feed_content() -> None:
    # feedparser accepts raw feed text directly, so no network is needed.
    entries = RSSCollector().collect(SAMPLE_FEED, max_entries=10)
    assert [e.title for e in entries] == ["AI breakthrough", "Robotics news"]
    assert entries[0].url == "https://example.com/a"
    assert entries[0].source_name == "Test Feed"


def test_load_rss_sources_skips_comments_and_blanks(tmp_path: Path) -> None:
    sources_file = tmp_path / "rss_sources.txt"
    sources_file.write_text(
        "# comment\n\nhttps://example.com/a.xml\n  \nhttps://example.com/b.xml\n",
        encoding="utf-8",
    )
    assert load_rss_sources(sources_file) == [
        "https://example.com/a.xml",
        "https://example.com/b.xml",
    ]
    assert load_rss_sources(tmp_path / "missing.txt") == []


def test_ingest_rss_candidates_dedupes_by_url(tmp_path: Path) -> None:
    db = StateDB(tmp_path / "state.sqlite3")
    entries = [
        RSSEntry(title="AI breakthrough", url="https://example.com/a", source_name="Feed"),
        RSSEntry(title="Robotics news", url="https://example.com/b", source_name="Feed"),
    ]
    assert db.ingest_rss_candidates(entries) == 2
    # Re-fetching the same feed must not pile up duplicates.
    assert db.ingest_rss_candidates(entries) == 0

    first = db.next_rss_candidate()
    assert first is not None
    db.mark_rss_candidate(first["url"], "used")
    second = db.next_rss_candidate()
    assert second is not None and second["url"] != first["url"]
    db.mark_rss_candidate(second["url"], "used")
    assert db.next_rss_candidate() is None


def test_plan_rss_action_builds_create_page(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "vault")
    db = StateDB(vault.root / ".agent-state.sqlite3")
    db.ingest_rss_candidates(
        [RSSEntry(title="量子ネットワークの新技術", url="https://example.com/q", source_name="Feed")]
    )
    # No sources file -> load_rss_sources returns [] and no network fetch happens.
    config = Config(tmp_path / "vault", rss_enabled=True, rss_sources_file=tmp_path / "none.txt")

    action = plan_rss_action(vault, db, config)

    assert action is not None
    assert action["action"] == "create_page"
    assert action["search_queries"] == ["量子ネットワークの新技術"]
    assert action["rss_url"] == "https://example.com/q"
    # The candidate is consumed so the next run does not repeat it.
    assert db.next_rss_candidate() is None


def test_plan_rss_action_redirects_duplicate_to_improve(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "vault")
    vault.write("10_Knowledge/量子ネットワーク.md", "# 量子ネットワーク\n\n既存ページ")
    db = StateDB(vault.root / ".agent-state.sqlite3")
    db.ingest_rss_candidates(
        [RSSEntry(title="量子ネットワーク", url="https://example.com/q", source_name="Feed")]
    )
    config = Config(tmp_path / "vault", rss_enabled=True, rss_sources_file=tmp_path / "none.txt")

    action = plan_rss_action(vault, db, config)

    assert action is not None
    assert action["action"] == "improve_page"
    assert Path(action["target"]) == Path("10_Knowledge/量子ネットワーク.md")


def test_plan_rss_action_returns_none_when_disabled(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "vault")
    db = StateDB(vault.root / ".agent-state.sqlite3")
    db.ingest_rss_candidates(
        [RSSEntry(title="AI", url="https://example.com/a", source_name="Feed")]
    )
    config = Config(tmp_path / "vault", rss_enabled=False)
    assert plan_rss_action(vault, db, config) is None


def test_run_once_rss_drives_page_creation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import src.wiki_agent as wiki_agent

    vault = Vault(tmp_path / "vault")
    db = StateDB(vault.root / ".agent-state.sqlite3")
    db.ingest_rss_candidates(
        [RSSEntry(title="ニューロモーフィック計算", url="https://example.com/n", source_name="Feed")]
    )
    config = Config(
        tmp_path / "vault",
        mode="autonomous_safe",
        rss_enabled=True,
        rss_sources_file=tmp_path / "none.txt",
    )

    fake = _FakeClient([])
    monkeypatch.setattr(wiki_agent, "create_client", lambda _config: fake)
    monkeypatch.setattr(Researcher, "search", lambda self, query, count=3: [])

    result = run_once(config)

    assert result["result"] == "success"
    assert result["action"]["action"] == "create_page"
    created = Vault(config.vault_path).safe(result["action"]["target"])
    assert created.exists()
    # The RSS candidate was consumed by the run.
    assert db.next_rss_candidate() is None
