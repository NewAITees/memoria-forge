from __future__ import annotations

from pathlib import Path

from src.memory_ingest import ingest_markdown_vault
from src.memory_store import MemoryStore


def test_markdown_vault_ingest_is_versioned_searchable_and_idempotent(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    note = vault / "Notes" / "Memory Graph.md"
    note.parent.mkdir(parents=True)
    note.write_bytes("# Memory Graph\n\nFacts connect through evidence.".encode("utf-8"))

    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        first = ingest_markdown_vault(store, vault)
        assert first.files_seen == 1
        assert first.imported_count == 1
        assert first.unchanged_count == 0
        assert first.skipped == ()
        assert len(first.source_ids) == 1

        source = store.connection.execute(
            "SELECT source_uri, title, media_type, raw_content FROM source_documents"
        ).fetchone()
        assert source == (
            "vault:/Notes/Memory%20Graph.md",
            "Memory Graph",
            "text/markdown",
            "# Memory Graph\n\nFacts connect through evidence.",
        )
        assert store.search_sources("connect evidence")[0].source_id == first.source_ids[0]
        assert store.connection.execute(
            "SELECT status FROM dream_jobs WHERE job_key = ?",
            (f"source:{first.source_ids[0]}",),
        ).fetchone() == ("pending",)

        repeated = ingest_markdown_vault(store, vault)
        assert repeated.imported_count == 0
        assert repeated.unchanged_count == 1
        assert repeated.source_ids == first.source_ids
        assert store.connection.execute("SELECT COUNT(*) FROM source_documents").fetchone()[0] == 1
        assert store.connection.execute("SELECT COUNT(*) FROM dream_jobs").fetchone()[0] == 1


def test_markdown_revision_creates_new_source_version_and_dream_job(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    note = vault / "Architecture.md"
    vault.mkdir()
    note.write_text("The store uses SQLite.", encoding="utf-8")

    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        before = ingest_markdown_vault(store, vault)
        note.write_text("The store uses SQLite with FTS.", encoding="utf-8")
        after = ingest_markdown_vault(store, vault)

        assert before.source_ids != after.source_ids
        assert after.imported_count == 1
        rows = store.connection.execute(
            "SELECT source_uri, content_sha256 FROM source_documents ORDER BY ingested_at"
        ).fetchall()
        assert len(rows) == 2
        assert {row[0] for row in rows} == {"vault:/Architecture.md"}
        assert store.connection.execute("SELECT COUNT(*) FROM dream_jobs").fetchone()[0] == 2


def test_markdown_vault_ingest_skips_hidden_state_empty_and_invalid_files(
    tmp_path: Path,
) -> None:
    vault = tmp_path / "vault"
    (vault / ".obsidian").mkdir(parents=True)
    (vault / "Visible").mkdir()
    (vault / ".hidden.md").write_text("hidden", encoding="utf-8")
    (vault / ".obsidian" / "workspace.md").write_text("state", encoding="utf-8")
    (vault / "Visible" / "empty.md").write_bytes(b" \n\t")
    (vault / "Visible" / "broken.md").write_bytes(b"\xff\xfe\xfa")
    (vault / "Visible" / "kept.md").write_text("Useful source content.", encoding="utf-8")
    (vault / "Visible" / ".memory-engine.sqlite3").write_bytes(b"not markdown content")

    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        result = ingest_markdown_vault(store, vault)

        assert result.files_seen == 3
        assert result.imported_count == 1
        assert result.skipped_count == 2
        assert {skip.reason for skip in result.skipped} == {
            "empty_markdown",
            "invalid_utf8",
        }
        assert store.connection.execute("SELECT COUNT(*) FROM source_documents").fetchone()[0] == 1
        assert (
            store.connection.execute("SELECT source_uri FROM source_documents").fetchone()[0]
            == "vault:/Visible/kept.md"
        )
