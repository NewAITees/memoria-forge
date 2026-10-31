import json
from pathlib import Path

import pytest

import run_agent
from src.memory_store import MemoryStore


def _config(tmp_path: Path) -> tuple[Path, Path]:
    vault = tmp_path / "vault"
    vault.mkdir()
    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"vault_path": str(vault)}), encoding="utf-8")
    return config_path, vault


def test_memory_sources_cli_lists_source_ids(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    config_path, vault = _config(tmp_path)
    with MemoryStore(vault / ".memory-engine.sqlite3") as store:
        source = store.add_source("note://listed", "A source for the CLI.", title="Listed")

    monkeypatch.setattr(
        "sys.argv", ["run_agent.py", "--config", str(config_path), "--memory-sources"]
    )
    run_agent.main()

    output = json.loads(capsys.readouterr().out)
    assert output[0]["source_id"] == source.source_id
    assert output[0]["source_uri"] == "note://listed"


def test_memory_erase_cli_requires_explicit_confirmation(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path, vault = _config(tmp_path)
    with MemoryStore(vault / ".memory-engine.sqlite3") as store:
        source = store.add_source("note://protected", "Retain until confirmed.")

    monkeypatch.setattr(
        "sys.argv",
        ["run_agent.py", "--config", str(config_path), "--memory-erase-source", source.source_id],
    )
    with pytest.raises(SystemExit) as error:
        run_agent.main()
    assert error.value.code == 2

    with MemoryStore(vault / ".memory-engine.sqlite3") as store:
        assert (
            store.connection.execute(
                "SELECT raw_content FROM source_documents WHERE source_id = ?", (source.source_id,)
            ).fetchone()[0]
            == "Retain until confirmed."
        )


def test_memory_erase_cli_requires_source_when_confirmation_given(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config_path, _vault = _config(tmp_path)
    monkeypatch.setattr(
        "sys.argv", ["run_agent.py", "--config", str(config_path), "--confirm-memory-erase"]
    )
    with pytest.raises(SystemExit) as error:
        run_agent.main()
    assert error.value.code == 2


def test_confirmed_memory_erase_cli_deletes_source_versions_and_jobs(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    config_path, vault = _config(tmp_path)
    with MemoryStore(vault / ".memory-engine.sqlite3") as store:
        first = store.add_source("note://erase-me", "The older content.")
        latest = store.add_source("note://erase-me", "The revised content.")

    monkeypatch.setattr(
        "sys.argv",
        [
            "run_agent.py",
            "--config",
            str(config_path),
            "--memory-erase-source",
            latest.source_id,
            "--confirm-memory-erase",
        ],
    )
    run_agent.main()

    output = json.loads(capsys.readouterr().out)
    assert output["result"] == "source_erased"
    assert output["source_id"] == latest.source_id
    with MemoryStore(vault / ".memory-engine.sqlite3") as store:
        assert (
            store.connection.execute(
                "SELECT COUNT(*) FROM source_documents WHERE source_uri = 'note://erase-me'"
            ).fetchone()[0]
            == 0
        )
        assert (
            store.connection.execute(
                "SELECT COUNT(*) FROM dream_jobs WHERE job_key IN (?, ?)",
                (f"source:{first.source_id}", f"source:{latest.source_id}"),
            ).fetchone()[0]
            == 0
        )
