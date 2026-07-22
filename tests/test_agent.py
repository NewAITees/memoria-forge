from pathlib import Path

import pytest

from src.wiki_agent import Config, Researcher, Vault, choose_candidate, validate_action


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
