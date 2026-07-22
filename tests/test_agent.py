import subprocess
from pathlib import Path

import pytest

from src.wiki_agent import (
    Config,
    Git,
    Researcher,
    Vault,
    choose_candidate,
    find_similar_page,
    process_lock,
    review_is_blocking,
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
