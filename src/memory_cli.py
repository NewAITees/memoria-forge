"""Command operations for inspecting and explicitly erasing memory sources."""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from typing import Any

from src.memory_store import MemoryStore


def run_source_command(vault_path: Path, source_id: str | None = None) -> Any:
    """List sources, or erase the selected source URI and its derived records.

    The caller owns confirmation policy; this function performs only the requested
    operation and returns JSON-serializable data for the CLI.
    """
    with MemoryStore(vault_path / ".memory-engine.sqlite3") as store:
        if source_id is None:
            return [asdict(source) for source in store.list_sources()]
        result = store.erase_source(source_id)
        return {
            "result": "source_erased",
            "source_id": source_id,
            **asdict(result),
        }
