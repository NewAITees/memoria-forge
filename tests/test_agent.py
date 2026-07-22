from pathlib import Path

import pytest

from src.wiki_agent import (
    Config,
    Researcher,
    Vault,
    choose_candidate,
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
