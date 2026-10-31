"""Persistence adapters for external source material in the local memory store."""

from __future__ import annotations

import hashlib
import json
import logging
import sqlite3
from pathlib import Path
from typing import Any

from src.memory_store import MemoryStore

logger = logging.getLogger(__name__)


def persist_documents(
    vault_path: Path,
    documents: list[tuple[str, str, str, str, str | None]],
) -> None:
    """Store non-empty source documents; failures never abort Wiki generation."""
    if not documents:
        return
    try:
        with MemoryStore(vault_path / ".memory-engine.sqlite3") as store:
            for uri, title, content, media_type, document_at in documents:
                if not uri.strip() or not content.strip():
                    continue
                try:
                    store.add_source(
                        uri,
                        content,
                        title=title,
                        media_type=media_type,
                        document_at=document_at,
                    )
                except (OSError, ValueError, sqlite3.Error) as error:
                    logger.warning("memory source ingest skipped uri=%s: %s", uri, error)
    except (OSError, ValueError, sqlite3.Error) as error:
        logger.warning("memory source store unavailable: %s", error)


def persist_rss_entries(vault_path: Path, entries: list[Any]) -> None:
    """Persist RSS article bodies, never using a summary as a substitute."""
    documents = [
        (
            entry.url,
            entry.title,
            entry.content,
            "text/x-rss-entry",
            entry.published_at.isoformat() if entry.published_at else None,
        )
        for entry in entries
        if entry.content.strip()
    ]
    persist_documents(vault_path, documents)


def persist_deep_research(vault_path: Path, records: list[dict[str, Any]]) -> None:
    """Store complete serialized Deep Research records under stable source IDs."""
    documents: list[tuple[str, str, str, str, str | None]] = []
    for record in records:
        source_uri = str(record.get("url", "")).strip()
        if not source_uri:
            continue
        record_json = json.dumps(record, ensure_ascii=False, sort_keys=True)
        record_id = hashlib.sha256(source_uri.encode("utf-8")).hexdigest()
        documents.append(
            (
                f"deep-research://{record_id}",
                f"Deep Research: {record.get('title') or source_uri}",
                record_json,
                "application/vnd.memoria.deep-research+json",
                None,
            )
        )
    persist_documents(vault_path, documents)
