import os
import subprocess
import tempfile
import time
from pathlib import Path

import pytest

from src.wiki_agent import (
    Config,
    Git,
    LMStudio,
    Ollama,
    Researcher,
    StateDB,
    Vault,
    choose_candidate,
    cohesion,
    commit_and_push,
    build_cluster_context,
    cosine,
    create_client,
    create_reviewer_client,
    find_similar_page,
    geometry_menu,
    ingest_rss,
    plan_geometry_action,
    normalize_new_page_target,
    plan_rss_action,
    process_lock,
    resolve_target_for_duplicates,
    review_is_blocking,
    run_once,
    running_mean,
    safe_new_page_target,
    strip_markdown_fence,
    two_means,
    unescape_literal_newlines,
    update_world_map,
    validate_action,
    REVIEW_RESPONSE_SCHEMA,
    WRITE_RESPONSE_SCHEMA,
)
from src.rss_collector import RSSCollector, RSSEntry, load_rss_sources
from run_agent import run_once_with_timeout, scheduled_lock_path
from src.research.deep_research import research_article


def test_vault_rejects_escape(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "vault")
    with pytest.raises(ValueError):
        vault.safe("../outside.md")


def test_empty_vault_gets_creation_candidate(tmp_path: Path) -> None:
    candidate = choose_candidate(Vault(tmp_path / "vault"))
    assert candidate["action"] == "create_page"


def test_choose_candidate_skips_recently_improved_smallest_page(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "vault")
    small = vault.write("10_Knowledge/small.md", "# small")
    big = vault.write("10_Knowledge/big.md", "# big\n\n" + "x" * 500)
    now = time.time()
    os.utime(small, (now, now))  # just improved -> inside the cooldown window
    os.utime(big, (now - 48 * 3600, now - 48 * 3600))  # eligible (48h old)

    candidate = choose_candidate(vault, improve_cooldown_hours=24)

    assert candidate["action"] == "improve_page"
    # The small page would normally win on size, but it is skipped during cooldown.
    assert candidate["target"].endswith("big.md")


def test_choose_candidate_round_robins_when_all_pages_recent(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "vault")
    newer = vault.write("10_Knowledge/newer.md", "# newer")
    older = vault.write("10_Knowledge/older.md", "# older\n\n" + "x" * 500)
    now = time.time()
    os.utime(newer, (now, now))
    os.utime(older, (now - 3600, now - 3600))  # 1h ago, still within cooldown

    candidate = choose_candidate(vault, improve_cooldown_hours=24)

    # Every page is recent, so pick the least recently updated one, not the smallest.
    assert candidate["target"].endswith("older.md")


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


def test_process_lock_reclaims_dead_pid(tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """A lock left by a crashed run (pid gone) is reclaimed, not blocked forever."""
    lock_path = tmp_path / ".agent-run.lock"
    lock_path.write_text("999999")
    monkeypatch.setattr("src.wiki_agent._pid_alive", lambda pid: False)
    with process_lock(lock_path) as acquired:
        assert acquired
    assert not lock_path.exists()


def test_process_lock_respects_live_pid(tmp_path: Path, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    """A lock owned by a live pid is preserved and the run is skipped."""
    lock_path = tmp_path / ".agent-run.lock"
    lock_path.write_text("4321")
    monkeypatch.setattr("src.wiki_agent._pid_alive", lambda pid: True)
    with process_lock(lock_path) as acquired:
        assert not acquired
    assert lock_path.exists()


def test_process_lock_keeps_unparseable_lock(tmp_path: Path) -> None:
    """An empty/garbage lock (owner unknown) is left in place, run skipped."""
    lock_path = tmp_path / ".agent-run.lock"
    lock_path.write_text("")
    with process_lock(lock_path) as acquired:
        assert not acquired
    assert lock_path.exists()


def test_scheduled_lock_path_is_outside_vault(tmp_path: Path) -> None:
    config = Config(tmp_path / "vault")
    lock_path = scheduled_lock_path(config)
    assert config.vault_path not in lock_path.parents
    assert lock_path.parent == Path(tempfile.gettempdir())


def test_run_once_with_timeout_returns_worker_result(tmp_path: Path) -> None:
    config = Config(tmp_path / "vault", max_run_minutes=1)
    result = run_once_with_timeout(config)
    assert result["result"] in {"success", "proposal", "expanded", "no_new_pages"}


def test_commit_failure_does_not_fail_wiki_result(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    vault = Vault(tmp_path / "vault")
    config = Config(tmp_path / "vault", git_enabled=True, auto_commit=True)
    monkeypatch.setattr(Git, "is_repo", lambda self: True)
    monkeypatch.setattr(Git, "status", lambda self: " M note.md")
    monkeypatch.setattr(
        Git,
        "commit",
        lambda self, message: (_ for _ in ()).throw(subprocess.CalledProcessError(128, "git")),
    )

    assert commit_and_push(vault, config, "wiki: test") == "commit_failed"


def test_deep_research_accepts_content_key_from_llm(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class Client:
        def chat(self, system: str, prompt: str) -> dict[str, object]:
            if "queries" in prompt:
                return {"queries": ["primary source"]}
            return {"content": "統合された調査結果"}

    class Search:
        def __init__(self, *args: object, **kwargs: object) -> None:
            pass

        def search(self, query: str, region: str = "jp-jp") -> list[dict[str, str]]:
            return [{"title": "Source", "url": "https://example.com", "snippet": "x" * 50}]

    monkeypatch.setattr("src.research.deep_research.DDGSearchClient", Search)
    monkeypatch.setattr(
        "src.research.deep_research.fetch_pages",
        lambda results, total_limit, per_page_limit: [
            {**results[0], "page_content": "evidence"}
        ],
    )

    result = research_article(Client(), title="Topic")

    assert result["synthesis"] == "統合された調査結果"


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


def test_typed_warning_with_blocking_keyword_is_not_escalated() -> None:
    # A warning must stay a warning even when its wording contains a blocking keyword.
    review = {
        "approved": False,
        "issues": [
            {"type": "warning", "description": "一部の主張に出典がないので confidence を下げてください。"},
            {"type": "warning", "description": "missing source title polish needed"},
        ],
    }
    assert not review_is_blocking(review)


def test_untyped_issue_with_blocking_keyword_still_blocks() -> None:
    # Untyped/malformed issues keep the keyword fallback so real problems are caught.
    assert review_is_blocking({"approved": False, "issues": ["missing sources"]})
    assert review_is_blocking({"approved": False, "issues": [{"type": "factual_error"}]})


def test_review_prompt_includes_today(monkeypatch: pytest.MonkeyPatch) -> None:
    from datetime import date

    captured: dict[str, str] = {}

    def fake_chat(
        self: Ollama, system: str, prompt: str, response_schema: object = None
    ) -> dict[str, object]:
        captured["prompt"] = prompt
        return {"approved": True, "issues": []}

    monkeypatch.setattr(Ollama, "chat", fake_chat)
    Ollama("http://localhost:11434", "qwen3:8b").review("# page")
    assert date.today().isoformat() in captured["prompt"]


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
        self,
        title: str,
        reason: str,
        sources: object,
        existing: str = "",
        feedback: str = "",
        research_context: str = "",
    ) -> str:
        return f"---\ntype: knowledge\nstatus: draft\n---\n\n# {title}\n\n## 概要\n\n{reason}\n"

    def review(self, content: str, research_context: str = "") -> dict[str, object]:
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
    monkeypatch.setattr(wiki_agent, "create_reviewer_client", lambda _config: fake)
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
    monkeypatch.setattr(wiki_agent, "create_reviewer_client", lambda _config: fake)
    monkeypatch.setattr(Researcher, "search", lambda self, query, count=3: [])

    result = run_once(config)

    # Previously this looped forever on plan_rejected and stalled the scheduler.
    assert result["result"] == "success"
    assert db.next_pending_task() is None
    created = Vault(config.vault_path).safe(result["action"]["target"])
    assert created.exists()
    assert Vault(config.vault_path).root in created.parents


def test_run_once_falls_back_when_planner_omits_target(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import src.wiki_agent as wiki_agent

    vault = Vault(tmp_path / "vault")
    vault.write("10_Knowledge/seed.md", "# seed\n\n本文")
    config = Config(tmp_path / "vault", mode="autonomous_safe")

    class TargetlessPlanner(_FakeClient):
        def plan(self, snapshot: object, stale: object = None) -> dict[str, object]:
            # Prose reason only, no target -- exactly what caused plan_rejected.
            return {"action": "improve_page", "reason": "改善案を提示します。"}

    fake = TargetlessPlanner([])
    monkeypatch.setattr(wiki_agent, "create_client", lambda _config: fake)
    monkeypatch.setattr(wiki_agent, "create_reviewer_client", lambda _config: fake)
    monkeypatch.setattr(Researcher, "search", lambda self, query, count=3: [])

    result = run_once(config)

    # Previously the targetless plan failed validation and repair, ending plan_rejected.
    assert result["result"] == "success"
    assert result["action"]["action"] == "improve_page"
    assert result["action"]["target"]


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
    monkeypatch.setattr(wiki_agent, "create_reviewer_client", lambda _config: fake)
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


def test_ingest_rss_candidate_preserves_article_metadata(tmp_path: Path) -> None:
    db = StateDB(tmp_path / "state.sqlite3")
    entry = RSSEntry(
        title="AI breakthrough",
        url="https://example.com/a",
        content="Article body",
        snippet="Short summary",
        source_name="Feed",
        feed_url="https://example.com/feed.xml",
        author="Author",
    )

    assert db.ingest_rss_candidates([entry]) == 1
    candidate = db.next_rss_candidate()

    assert candidate is not None
    assert candidate["content"] == "Article body"
    assert candidate["snippet"] == "Short summary"
    assert candidate["feed_url"] == "https://example.com/feed.xml"
    assert candidate["author"] == "Author"


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
    monkeypatch.setattr(wiki_agent, "create_reviewer_client", lambda _config: fake)
    monkeypatch.setattr(Researcher, "search", lambda self, query, count=3: [])

    result = run_once(config)

    assert result["result"] == "success"
    assert result["action"]["action"] == "create_page"
    created = Vault(config.vault_path).safe(result["action"]["target"])
    assert created.exists()
    # The RSS candidate was consumed by the run.
    assert db.next_rss_candidate() is None


def test_cosine_and_running_mean() -> None:
    assert cosine([1.0, 0.0], [1.0, 0.0]) == pytest.approx(1.0)
    assert cosine([1.0, 0.0], [0.0, 1.0]) == pytest.approx(0.0)
    assert cosine([0.0, 0.0], [1.0, 1.0]) == 0.0  # zero magnitude is safe, not a crash
    assert running_mean([2.0], 1, [4.0]) == [3.0]
    assert running_mean([0.0, 0.0], 3, [4.0, 8.0]) == [1.0, 2.0]


def test_assign_point_seeds_attaches_and_grows(tmp_path: Path) -> None:
    db = StateDB(tmp_path / "s.sqlite3")
    c1, new1 = db.assign_point("a", [1.0, 0.0, 0.0], 0.72)
    assert new1 is True
    c2, new2 = db.assign_point("b", [0.9, 0.1, 0.0], 0.72)  # near a
    assert new2 is False and c2 == c1
    c3, new3 = db.assign_point("c", [0.0, 1.0, 0.0], 0.72)  # far
    assert new3 is True and c3 != c1
    summary = db.cluster_summary()
    assert [s["size"] for s in summary] == [2, 1]


def test_update_world_map_assigns_then_is_idempotent(tmp_path: Path) -> None:
    db = StateDB(tmp_path / "s.sqlite3")
    for url, title in [("u1", "space one"), ("u2", "space two"), ("u3", "food item")]:
        db.db.execute(
            "INSERT INTO rss_candidates (url, title, snippet, status) VALUES (?, ?, ?, ?)",
            (url, title, "", "new"),
        )
    db.db.commit()
    vectors = {
        "space one": [1.0, 0.0, 0.0],
        "space two": [0.92, 0.08, 0.0],
        "food item": [0.0, 1.0, 0.0],
    }
    config = Config(vault_path=tmp_path / "v", embed_prompt="")
    first = update_world_map(db, config, embed_fn=lambda text: vectors[text])
    assert first == {"assigned": 3, "new_clusters": 2, "splits": 0, "merges": 0}
    assert [s["size"] for s in db.cluster_summary()] == [2, 1]
    # A second pass re-embeds nothing: every candidate is already on the map.
    second = update_world_map(db, config, embed_fn=lambda text: vectors[text])
    assert second == {"assigned": 0, "new_clusters": 0, "splits": 0, "merges": 0}


def test_two_means_and_cohesion_separate_two_blobs() -> None:
    vectors = [[1.0, 0.0], [0.98, 0.02], [0.0, 1.0], [0.02, 0.98]]
    labels = two_means(vectors)
    assert labels[0] == labels[1] and labels[2] == labels[3]
    assert labels[0] != labels[2]
    assert cohesion([[1.0, 0.0], [1.0, 0.0]]) == pytest.approx(1.0)
    assert cohesion(vectors) < 0.9  # a two-blob set is not cohesive


def test_consolidate_merges_near_duplicate_clusters(tmp_path: Path) -> None:
    db = StateDB(tmp_path / "s.sqlite3")
    # A high attach threshold forces two near (cos 0.9) points into separate clusters.
    db.assign_point("a", [1.0, 0.0], 0.99)
    db.assign_point("b", [0.9, 0.436], 0.99)
    assert len(db.cluster_summary()) == 2
    stats = db.consolidate(merge_threshold=0.86, split_cohesion=0.0, min_split_size=100)
    assert stats["merges"] == 1
    assert [s["size"] for s in db.cluster_summary()] == [2]


def test_consolidate_splits_a_dispersed_cluster(tmp_path: Path) -> None:
    db = StateDB(tmp_path / "s.sqlite3")
    blob = [[1.0, 0.0, 0.0], [0.95, 0.05, 0.0], [0.9, 0.1, 0.0],
            [0.0, 1.0, 0.0], [0.05, 0.95, 0.0], [0.1, 0.9, 0.0]]
    for i, v in enumerate(blob):  # attach threshold 0.0 forces one cluster
        db.assign_point(f"x{i}", v, 0.0)
    assert len(db.cluster_summary()) == 1
    stats = db.consolidate(merge_threshold=0.99, split_cohesion=0.9, min_split_size=6)
    assert stats["splits"] == 1
    assert sorted(s["size"] for s in db.cluster_summary()) == [3, 3]


def test_consolidate_preserves_paged_size(tmp_path: Path) -> None:
    # Regression: consolidate rewrites the clusters table every run; it must carry
    # paged_size through, or the convergence signal is wiped and a paged cluster is
    # re-improved forever.
    db = StateDB(tmp_path / "s.sqlite3")
    _seed_rss(db, [("a1", "x"), ("a2", "y")])
    cid, _ = db.assign_point("a1", [1.0, 0.0], 0.7)
    db.assign_point("a2", [0.99, 0.01], 0.7)
    db.link_cluster_page(cid, "10_Knowledge/x.md")  # paged_size = 2
    db.consolidate(merge_threshold=0.99, split_cohesion=0.0, min_split_size=100)  # no-op
    row = db.cluster_summary()[0]
    assert row["page_path"] == "10_Knowledge/x.md"
    assert row["paged_size"] == 2


def _seed_rss(db: StateDB, rows: list[tuple[str, str]]) -> None:
    for url, title in rows:
        db.db.execute(
            "INSERT INTO rss_candidates (url, title, snippet, status) VALUES (?, ?, ?, ?)",
            (url, title, "", "new"),
        )
    db.db.commit()


def test_cluster_representative_title_is_founding_member(tmp_path: Path) -> None:
    db = StateDB(tmp_path / "s.sqlite3")
    _seed_rss(db, [("u1", "量子コンピュータ"), ("u2", "量子誤り訂正")])
    cid, _ = db.assign_point("u1", [1.0, 0.0], 0.7)
    db.assign_point("u2", [0.99, 0.01], 0.7)  # attaches to the same cluster
    assert db.cluster_representative_title(cid) == ("u1", "量子コンピュータ")
    assert db.cluster_representative_title(999) is None


def test_geometry_menu_creates_for_dense_unpaged_and_skips_frontier(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "v")
    db = StateDB(vault.root / ".agent-state.sqlite3")
    config = Config(vault_path=vault.root, cluster_page_min_size=2)
    _seed_rss(db, [("a1", "AI規制"), ("a2", "AI倫理"), ("b1", "EV電池")])
    db.assign_point("a1", [1.0, 0.0], 0.7)  # dense cluster (>= K): create
    db.assign_point("a2", [0.99, 0.01], 0.7)
    db.assign_point("b1", [0.0, 1.0], 0.7)  # lone point (< K): frontier, skipped
    menu = geometry_menu(vault, db, config)
    assert len(menu) == 1
    assert menu[0]["action"] == "create_page"
    assert menu[0]["search_queries"] == ["AI規制"]
    assert menu[0]["cluster_id"] is not None


def test_geometry_menu_improves_paged_cluster(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "v")
    db = StateDB(vault.root / ".agent-state.sqlite3")
    config = Config(vault_path=vault.root, cluster_page_min_size=2)
    _seed_rss(db, [("p1", "話題")])
    cid, _ = db.assign_point("p1", [1.0, 0.0], 0.7)  # size 1, but paged -> improve
    page = vault.root / "10_Knowledge" / "既存.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text("x", encoding="utf-8")
    db.db.execute(
        "UPDATE clusters SET page_path = ? WHERE cluster_id = ?", ("10_Knowledge/既存.md", cid)
    )
    db.db.commit()
    menu = geometry_menu(vault, db, config)
    assert len(menu) == 1
    assert menu[0]["action"] == "improve_page"
    assert menu[0]["target"] == "10_Knowledge/既存.md"


def test_plan_geometry_action_none_when_map_empty(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "v")
    db = StateDB(vault.root / ".agent-state.sqlite3")
    assert plan_geometry_action(vault, db, Config(vault_path=vault.root)) is None


def test_geometry_planner_defaults_off_and_validates(tmp_path: Path) -> None:
    config = Config(vault_path=tmp_path / "v")
    assert config.geometry_planner is False
    config.validate()


def test_ingest_rss_returns_zero_when_disabled(tmp_path: Path) -> None:
    db = StateDB(tmp_path / "s.sqlite3")
    config = Config(vault_path=tmp_path / "v", rss_enabled=False)
    assert ingest_rss(db, config) == 0


def test_link_cluster_page_converges_then_improves_only_after_growth(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "v")
    db = StateDB(vault.root / ".agent-state.sqlite3")
    config = Config(vault_path=vault.root, cluster_page_min_size=2)
    _seed_rss(db, [("a1", "AI規制"), ("a2", "AI倫理"), ("a3", "AI著作権")])
    cid, _ = db.assign_point("a1", [1.0, 0.0], 0.7)
    db.assign_point("a2", [0.99, 0.01], 0.7)
    assert geometry_menu(vault, db, config)[0]["action"] == "create_page"
    # A page is produced for the cluster; the identity loop binds them at size 2.
    page = vault.root / "10_Knowledge" / "AI.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text("x", encoding="utf-8")
    db.link_cluster_page(cid, "10_Knowledge/AI.md")
    # Converged: no growth since the page was written -> nothing to do.
    assert geometry_menu(vault, db, config) == []
    # A new point lands in the cluster -> now (and only now) it is worth improving.
    db.assign_point("a3", [0.98, 0.02], 0.7)
    top = geometry_menu(vault, db, config)[0]
    assert top["action"] == "improve_page"
    assert top["target"] == "10_Knowledge/AI.md"


def test_geometry_menu_prioritizes_frontier_create_over_grown_improve(tmp_path: Path) -> None:
    vault = Vault(tmp_path / "v")
    db = StateDB(vault.root / ".agent-state.sqlite3")
    config = Config(vault_path=vault.root, cluster_page_min_size=2)
    _seed_rss(db, [("a1", "AI"), ("a2", "AI2"), ("a3", "AI3"), ("b1", "宇宙"), ("b2", "宇宙2")])
    # Paged cluster A that has since grown (an improve candidate).
    cid_a, _ = db.assign_point("a1", [1.0, 0.0], 0.7)
    db.assign_point("a2", [0.99, 0.01], 0.7)
    page = vault.root / "10_Knowledge" / "AI.md"
    page.parent.mkdir(parents=True, exist_ok=True)
    page.write_text("x", encoding="utf-8")
    db.link_cluster_page(cid_a, "10_Knowledge/AI.md")  # paged_size = 2
    db.assign_point("a3", [0.98, 0.02], 0.7)  # grows to 3 -> improve candidate
    # Unpaged dense cluster B (a create candidate) must be picked first.
    db.assign_point("b1", [0.0, 1.0], 0.7)
    db.assign_point("b2", [0.01, 0.99], 0.7)
    top = geometry_menu(vault, db, config)[0]
    assert top["action"] == "create_page" and top["cluster_id"] == cid_a + 1


def test_link_cluster_page_records_paged_size(tmp_path: Path) -> None:
    db = StateDB(tmp_path / "s.sqlite3")
    _seed_rss(db, [("a1", "x"), ("a2", "y")])
    cid, _ = db.assign_point("a1", [1.0, 0.0], 0.7)
    db.assign_point("a2", [0.99, 0.01], 0.7)  # size 2
    db.link_cluster_page(cid, "10_Knowledge/x.md")
    row = db.cluster_summary()[0]
    assert row["page_path"] == "10_Knowledge/x.md" and row["paged_size"] == 2


def test_cluster_research_aggregates_member_deep_research(tmp_path: Path) -> None:
    db = StateDB(tmp_path / "s.sqlite3")
    _seed_rss(db, [("u1", "t1"), ("u2", "t2")])
    cid, _ = db.assign_point("u1", [1.0, 0.0], 0.7)
    db.assign_point("u2", [0.99, 0.01], 0.7)
    db.save_deep_research(
        "u1",
        {
            "queries": ["q1"],
            "results": [{"title": "R1", "url": "http://r1", "snippet": "s", "page_content": "body1"}],
            "synthesis": "syn1",
        },
    )
    assert db.cluster_member_urls(cid) == ["u1", "u2"]
    research = db.cluster_research(cid)  # only u1 has been researched
    assert len(research) == 1
    assert research[0]["url"] == "u1" and research[0]["synthesis"] == "syn1"
    assert research[0]["results"][0]["title"] == "R1"


def test_build_cluster_context_uses_existing_research_without_network(tmp_path: Path) -> None:
    db = StateDB(tmp_path / "s.sqlite3")
    _seed_rss(db, [("u1", "t1")])
    cid, _ = db.assign_point("u1", [1.0, 0.0], 0.7)
    db.save_deep_research(
        "u1",
        {
            "queries": ["q1", "q2"],
            "results": [{"title": "R1", "url": "http://r1", "snippet": "snip", "page_content": "body"}],
            "synthesis": "syn1",
        },
    )
    config = Config(vault_path=tmp_path / "v")

    class FakeClient:
        def chat(self, system: str, prompt: str) -> dict[str, object]:
            raise AssertionError("no member should need on-demand research here")

    context, sources, new_searches = build_cluster_context(db, FakeClient(), cid, config)
    assert "syn1" in context and "body" in context
    assert len(sources) == 1 and sources[0].url == "http://r1"
    assert new_searches == 0  # nothing new researched, so no searches counted this run


def test_write_passes_content_schema_to_chat() -> None:
    captured: dict[str, object] = {}

    class Probe(Ollama):
        def chat(
            self, system: str, prompt: str, response_schema: object = None
        ) -> dict[str, object]:
            captured["schema"] = response_schema
            return {"content": "# ok\n\nbody"}

    out = Probe("http://x", "m").write("題", "理由", [])
    assert captured["schema"] == WRITE_RESPONSE_SCHEMA  # keys are pinned, not free-form json
    assert "# ok" in out


class _EmptyThenValidWriter:
    """Autonomous client whose writer returns empty content the first N calls."""

    def __init__(self, empty_times: int) -> None:
        self.empty_times = empty_times
        self.calls = 0

    def plan(self, snapshot: object, stale: object = None) -> dict[str, object]:
        # No target -> run_once falls back to the deterministic improve candidate.
        return {"action": "improve_page", "reason": "更新する"}

    def write(
        self,
        title: str,
        reason: str,
        sources: object,
        existing: str = "",
        feedback: str = "",
        research_context: str = "",
    ) -> str:
        self.calls += 1
        if self.calls <= self.empty_times:
            raise ValueError("writer returned no content")
        return f"---\ntype: knowledge\nstatus: draft\n---\n\n# {title}\n\n## 概要\n\n{reason}\n"

    def review(self, content: str, research_context: str = "") -> dict[str, object]:
        return {"approved": True, "issues": []}


def test_run_once_recovers_when_writer_is_empty_once(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import src.wiki_agent as wiki_agent

    vault = Vault(tmp_path / "vault")
    vault.write("10_Knowledge/seed.md", "# seed\n\nbody")
    config = Config(tmp_path / "vault", mode="autonomous_safe")
    fake = _EmptyThenValidWriter(empty_times=1)
    monkeypatch.setattr(wiki_agent, "create_client", lambda _config: fake)
    monkeypatch.setattr(wiki_agent, "create_reviewer_client", lambda _config: fake)
    monkeypatch.setattr(Researcher, "search", lambda self, query, count=3: [])

    result = run_once(config)

    assert result["result"] == "success"  # a single empty generation is retried, not fatal
    assert fake.calls == 2


def test_run_once_reports_review_rejected_when_writer_stays_empty(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import src.wiki_agent as wiki_agent

    vault = Vault(tmp_path / "vault")
    vault.write("10_Knowledge/seed.md", "# seed\n\nbody")
    config = Config(tmp_path / "vault", mode="autonomous_safe")
    fake = _EmptyThenValidWriter(empty_times=2)
    monkeypatch.setattr(wiki_agent, "create_client", lambda _config: fake)
    monkeypatch.setattr(wiki_agent, "create_reviewer_client", lambda _config: fake)
    monkeypatch.setattr(Researcher, "search", lambda self, query, count=3: [])

    result = run_once(config)

    # The whole run no longer crashes on persistent empty output; it records cleanly.
    assert result["result"] == "review_rejected"
    assert fake.calls == 2


def test_create_reviewer_client_uses_review_model_when_set(tmp_path: Path) -> None:
    base = Config(tmp_path / "v", model="qwen3:8b")
    assert create_reviewer_client(base).model == "qwen3:8b"  # empty -> writer model
    separated = Config(tmp_path / "v", model="qwen3:8b", review_model="gemma3:4b")
    assert create_reviewer_client(separated).model == "gemma3:4b"


def test_review_passes_review_schema_to_chat() -> None:
    captured: dict[str, object] = {}

    class Probe(Ollama):
        def chat(
            self, system: str, prompt: str, response_schema: object = None
        ) -> dict[str, object]:
            captured["schema"] = response_schema
            return {"approved": True, "issues": []}

    Probe("http://x", "m").review("# page")
    assert captured["schema"] == REVIEW_RESPONSE_SCHEMA


def test_run_once_reviews_with_separate_reviewer_client(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    import src.wiki_agent as wiki_agent

    vault = Vault(tmp_path / "vault")
    vault.write("10_Knowledge/seed.md", "# seed\n\nbody")
    config = Config(tmp_path / "vault", mode="autonomous_safe", review_model="gemma3:4b")

    class Writer:
        def __init__(self) -> None:
            self.reviews = 0

        def plan(self, snapshot: object, stale: object = None) -> dict[str, object]:
            return {"action": "improve_page", "reason": "更新する"}

        def write(self, *args: object, **kwargs: object) -> str:
            return "---\ntype: knowledge\nstatus: draft\n---\n\n# T\n\n## 概要\n\n本文\n"

        def review(self, content: str, research_context: str = "") -> dict[str, object]:
            self.reviews += 1
            return {"approved": True, "issues": []}

    class Reviewer:
        def __init__(self) -> None:
            self.reviews = 0

        def review(self, content: str, research_context: str = "") -> dict[str, object]:
            self.reviews += 1
            return {"approved": True, "issues": []}

    writer, reviewer = Writer(), Reviewer()
    monkeypatch.setattr(wiki_agent, "create_client", lambda _config: writer)
    monkeypatch.setattr(wiki_agent, "create_reviewer_client", lambda _config: reviewer)
    monkeypatch.setattr(Researcher, "search", lambda self, query, count=3: [])

    result = run_once(config)

    assert result["result"] == "success"
    # The page was judged by the separate reviewer, never the writer itself.
    assert reviewer.reviews == 1 and writer.reviews == 0
