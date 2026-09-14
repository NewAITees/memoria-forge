"""Build deterministic Maps of Content from clusters linked to Markdown pages."""

from __future__ import annotations

import hashlib
import json
import math
import sqlite3
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

GENERATED_MARKER = "generated_by: memoria-forge-moc"
PAGE_EMBED_PROMPT = "task: clustering | query: Markdown knowledge page: "


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def normalize(vector: list[float]) -> list[float]:
    norm = math.sqrt(dot(vector, vector))
    return [value / norm for value in vector] if norm else vector[:]


def sync_page_embeddings(
    vault: Path,
    database: Path,
    embed_fn: Any,
    prompt: str = PAGE_EMBED_PROMPT,
) -> dict[str, int]:
    """Embed changed knowledge Markdown and retain unchanged vectors by content hash."""
    connection = sqlite3.connect(database, timeout=30)
    connection.execute("PRAGMA busy_timeout = 30000")
    connection.execute("""
        CREATE TABLE IF NOT EXISTS page_embeddings (
            page_path TEXT PRIMARY KEY,
            content_hash TEXT NOT NULL,
            embedding TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    paths = sorted(
        path for path in vault.rglob("*.md") if "20_MOC" not in path.relative_to(vault).parts
    )
    active_paths: set[str] = set()
    updated = 0
    cached = 0
    timestamp = datetime.now(timezone.utc).isoformat()
    for path in paths:
        relative = str(path.relative_to(vault)).replace("\\", "/")
        active_paths.add(relative)
        content = path.read_text(encoding="utf-8")
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        row = connection.execute(
            "SELECT content_hash FROM page_embeddings WHERE page_path = ?", (relative,)
        ).fetchone()
        if row and row[0] == content_hash:
            cached += 1
            continue
        embedding = embed_fn(prompt + path.stem + "\n" + content[:16000])
        values = (relative, content_hash, json.dumps(list(embedding)), timestamp)
        for attempt in range(6):
            try:
                connection.execute(
                    "INSERT OR REPLACE INTO page_embeddings VALUES (?, ?, ?, ?)", values
                )
                connection.commit()
                break
            except sqlite3.OperationalError as error:
                connection.rollback()
                if "locked" not in str(error).lower() or attempt == 5:
                    raise
                time.sleep(5)
        updated += 1
    if active_paths:
        placeholders = ",".join("?" for _ in active_paths)
        connection.execute(
            f"DELETE FROM page_embeddings WHERE page_path NOT IN ({placeholders})",
            tuple(sorted(active_paths)),
        )
    else:
        connection.execute("DELETE FROM page_embeddings")
    connection.commit()
    connection.close()
    return {"updated": updated, "cached": cached, "pages": len(paths)}


def group_pages(pages: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    """Group only strong or reciprocal-nearest Markdown relationships."""
    if len(pages) < 2:
        return []
    vectors = [normalize(page["embedding"]) for page in pages]
    nearest = [
        max((dot(vector, other), other_index) for other_index, other in enumerate(vectors) if index != other_index)
        for index, vector in enumerate(vectors)
    ]
    adjacency: dict[int, set[int]] = {index: set() for index in range(len(pages))}
    for index, (similarity, other_index) in enumerate(nearest):
        reciprocal = nearest[other_index][1] == index
        if similarity >= 0.9 or (reciprocal and similarity >= 0.8):
            adjacency[index].add(other_index)
            adjacency[other_index].add(index)
    groups: list[list[dict[str, Any]]] = []
    visited: set[int] = set()
    for start in range(len(pages)):
        if start in visited or not adjacency[start]:
            continue
        pending = [start]
        component: list[int] = []
        visited.add(start)
        while pending:
            current = pending.pop()
            component.append(current)
            for neighbor in sorted(adjacency[current]):
                if neighbor not in visited:
                    visited.add(neighbor)
                    pending.append(neighbor)
        groups.append([pages[index] for index in sorted(component)])
    return sorted(groups, key=lambda members: (-len(members), members[0]["page_path"]))


def wiki_link(page_path: str) -> str:
    return page_path.replace("\\", "/").removesuffix(".md")


def render_moc(moc_id: int, title: str, members: list[dict[str, Any]]) -> str:
    lines = [
        "---",
        "type: moc",
        GENERATED_MARKER,
        f"moc_id: {moc_id}",
        f"updated_at: {datetime.now(timezone.utc).isoformat()}",
        "---",
        "",
        f"# {title}",
        "",
        "## この領域の知識ページ",
        "",
    ]
    for member in members:
        cluster = (
            f" — クラスタ#{member['cluster_id']}・{member['size']}件"
            if member["cluster_id"] is not None
            else " — Markdown本文から分類"
        )
        lines.append(f"- [[{wiki_link(member['page_path'])}]]{cluster}")
    lines.extend(["", "## DBとの関係", "", f"- 所属Markdown数: {len(members)}", ""])
    return "\n".join(lines)


def build_mocs(vault: Path, database: Path, embed_fn: Any) -> dict[str, int]:
    """Persist MOC membership and generate only files owned by this builder."""
    embedding_stats = sync_page_embeddings(vault, database, embed_fn)
    connection = sqlite3.connect(database, timeout=30)
    connection.execute("PRAGMA busy_timeout = 30000")
    connection.executescript("""
        CREATE TABLE IF NOT EXISTS mocs (
            moc_id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            page_path TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        DROP TABLE IF EXISTS moc_members;
        CREATE TABLE moc_members (
            moc_id INTEGER NOT NULL,
            page_path TEXT NOT NULL PRIMARY KEY,
            cluster_id INTEGER,
            similarity REAL NOT NULL,
            FOREIGN KEY (moc_id) REFERENCES mocs(moc_id)
        );
    """)
    rows = connection.execute(
        """
        SELECT p.page_path, p.embedding, c.cluster_id, c.size
        FROM page_embeddings p
        LEFT JOIN clusters c ON REPLACE(c.page_path, '\\', '/') = p.page_path
        ORDER BY p.page_path
        """
    ).fetchall()
    pages = [
        {
            "page_path": str(page_path),
            "embedding": json.loads(embedding),
            "cluster_id": int(cluster_id) if cluster_id is not None else None,
            "size": int(size) if size is not None else 0,
        }
        for page_path, embedding, cluster_id, size in rows
        if (vault / str(page_path)).exists()
    ]
    groups = group_pages(pages)
    connection.execute("DELETE FROM moc_members")
    connection.execute("DELETE FROM mocs")
    moc_directory = vault / "20_MOC"
    moc_directory.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    generated_paths: set[Path] = set()
    for moc_id, members in enumerate(groups, 1):
        names = [Path(member["page_path"]).stem for member in members[:2]]
        title = "MOC — " + " / ".join(name[:32] for name in names)
        relative_path = f"20_MOC/MOC-{moc_id:03d}.md"
        target = vault / relative_path
        target.write_text(render_moc(moc_id, title, members), encoding="utf-8", newline="\n")
        generated_paths.add(target.resolve())
        connection.execute("INSERT INTO mocs VALUES (?, ?, ?, ?)", (moc_id, title, relative_path, now))
        center = normalize([
            sum(item["embedding"][axis] for item in members)
            for axis in range(len(members[0]["embedding"]))
        ])
        for member in members:
            connection.execute(
                "INSERT INTO moc_members VALUES (?, ?, ?, ?)",
                (moc_id, member["page_path"], member["cluster_id"], dot(normalize(member["embedding"]), center)),
            )

    for old_path in moc_directory.glob("MOC-*.md"):
        if old_path.resolve() not in generated_paths and GENERATED_MARKER in old_path.read_text(encoding="utf-8"):
            old_path.unlink()

    all_markdown = [
        path for path in vault.rglob("*.md") if "20_MOC" not in path.relative_to(vault).parts
    ]
    grouped_paths = {member["page_path"] for group in groups for member in group}
    unlinked_pages = [
        str(path.relative_to(vault)).replace("\\", "/")
        for path in all_markdown
        if str(path.relative_to(vault)).replace("\\", "/") not in grouped_paths
    ]
    unpromoted = connection.execute(
        "SELECT COUNT(*) FROM clusters WHERE page_path IS NULL"
    ).fetchone()[0]
    index_lines = [
        "---", "type: moc-index", GENERATED_MARKER, f"updated_at: {now}", "---", "",
        "# MOC一覧", "", "## 知識領域", "",
    ]
    for moc_id, members in enumerate(groups, 1):
        title = " / ".join(Path(member["page_path"]).stem[:32] for member in members[:2])
        index_lines.append(f"- [[20_MOC/MOC-{moc_id:03d}|{title}]] — {len(members)}ページ")
    index_lines.extend(["", "## 未整理の境界", "", f"- Markdown未昇格クラスタ: {unpromoted}", f"- MOC未所属Markdown: {len(unlinked_pages)}", ""])
    if unlinked_pages:
        index_lines.extend([f"- [[{wiki_link(path)}]]" for path in unlinked_pages])
        index_lines.append("")
    (moc_directory / "00_MOC一覧.md").write_text("\n".join(index_lines), encoding="utf-8", newline="\n")
    connection.commit()
    connection.close()
    return {
        "mocs": len(groups),
        "grouped_pages": len(grouped_paths),
        "unlinked_pages": len(unlinked_pages),
        "unpromoted_clusters": int(unpromoted),
        "embeddings_updated": embedding_stats["updated"],
    }
