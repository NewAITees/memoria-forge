"""Import Markdown documents from a Vault into the independent memory store."""

from __future__ import annotations

import os
import argparse
import json
from dataclasses import dataclass
from dataclasses import asdict
from pathlib import Path
from urllib.parse import quote

from src.memory_store import MemoryStore


def _is_hidden(path: Path) -> bool:
    if path.name.startswith("."):
        return True
    try:
        attributes = getattr(path.stat(follow_symlinks=False), "st_file_attributes", 0)
    except OSError:
        return False
    return bool(attributes & 0x2)


@dataclass(frozen=True)
class MarkdownIngestSkip:
    relative_path: str
    reason: str


@dataclass(frozen=True)
class MarkdownIngestResult:
    files_seen: int
    imported_count: int
    unchanged_count: int
    skipped: tuple[MarkdownIngestSkip, ...]
    source_ids: tuple[str, ...]

    @property
    def skipped_count(self) -> int:
        return len(self.skipped)


def ingest_markdown_vault(store: MemoryStore, vault_root: Path) -> MarkdownIngestResult:
    """Import visible Markdown files without following links or leaving the Vault root.

    The URI is based on the Vault-relative path, so file versions remain grouped when
    a document changes. Hidden paths and reparse/symlinked directories are excluded.
    """
    root = vault_root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("vault_root must be a directory")

    files_seen = 0
    imported = 0
    unchanged = 0
    skipped: list[MarkdownIngestSkip] = []
    source_ids: list[str] = []

    def record_walk_error(error: OSError) -> None:
        path = Path(error.filename) if error.filename else root
        try:
            relative = path.relative_to(root).as_posix()
        except ValueError:
            relative = "."
        skipped.append(MarkdownIngestSkip(relative, "directory_read_error"))

    for directory, directories, filenames in os.walk(
        root, topdown=True, followlinks=False, onerror=record_walk_error
    ):
        current = Path(directory)
        visible_directories: list[str] = []
        for name in sorted(directories):
            candidate = current / name
            if _is_hidden(candidate):
                continue
            if candidate.is_symlink() or candidate.is_junction():
                continue
            visible_directories.append(name)
        directories[:] = visible_directories

        for name in sorted(filenames):
            path = current / name
            if _is_hidden(path) or Path(name).suffix.casefold() != ".md":
                continue
            files_seen += 1
            relative_path = path.relative_to(root).as_posix()
            try:
                if path.is_symlink() or path.is_junction():
                    skipped.append(MarkdownIngestSkip(relative_path, "linked_file"))
                    continue
                resolved = path.resolve(strict=True)
                try:
                    resolved.relative_to(root)
                except ValueError:
                    skipped.append(MarkdownIngestSkip(relative_path, "outside_vault"))
                    continue
                content = path.read_bytes().decode("utf-8-sig")
            except UnicodeDecodeError:
                skipped.append(MarkdownIngestSkip(relative_path, "invalid_utf8"))
                continue
            except OSError:
                skipped.append(MarkdownIngestSkip(relative_path, "read_error"))
                continue

            if not content.strip():
                skipped.append(MarkdownIngestSkip(relative_path, "empty_markdown"))
                continue

            source_uri = "vault:/" + quote(relative_path, safe="/")
            result = store.add_source(
                source_uri,
                content,
                title=path.stem,
                media_type="text/markdown",
            )
            source_ids.append(result.source_id)
            if result.created:
                imported += 1
            else:
                unchanged += 1

    return MarkdownIngestResult(
        files_seen=files_seen,
        imported_count=imported,
        unchanged_count=unchanged,
        skipped=tuple(skipped),
        source_ids=tuple(source_ids),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Import visible Vault Markdown into local memory.")
    parser.add_argument("--config", type=Path, default=Path("config.json"))
    args = parser.parse_args()

    from src.wiki_agent import Config

    config = Config.load(args.config)
    with MemoryStore(config.vault_path / ".memory-engine.sqlite3") as store:
        result = ingest_markdown_vault(store, config.vault_path)
    print(json.dumps(asdict(result), ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
