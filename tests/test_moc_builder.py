import json
import sqlite3
from pathlib import Path

from src.moc_builder import GENERATED_MARKER, build_mocs, group_pages


def test_group_pages_keeps_only_reciprocal_nearest_neighbors() -> None:
    pages = [
        {"page_path": "a.md", "embedding": [1.0, 0.0]},
        {"page_path": "b.md", "embedding": [0.9, 0.1]},
        {"page_path": "c.md", "embedding": [0.0, 1.0]},
        {"page_path": "d.md", "embedding": [-1.0, 0.0]},
    ]
    groups = [[item["page_path"] for item in group] for group in group_pages(pages)]
    assert groups == [["a.md", "b.md"]]


def test_build_mocs_persists_relationships_and_writes_owned_files(tmp_path: Path) -> None:
    vault = tmp_path / "vault"
    knowledge = vault / "10_Knowledge"
    knowledge.mkdir(parents=True)
    (knowledge / "alpha.md").write_text("# Alpha", encoding="utf-8")
    (knowledge / "beta.md").write_text("# Beta", encoding="utf-8")
    database = vault / ".agent-state.sqlite3"
    connection = sqlite3.connect(database)
    connection.executescript("""
        CREATE TABLE clusters (cluster_id INTEGER, centroid TEXT, size INTEGER, page_path TEXT);
        CREATE TABLE cluster_members (url TEXT, cluster_id INTEGER, assigned_at TEXT);
        CREATE TABLE rss_candidates (url TEXT, title TEXT);
    """)
    connection.executemany(
        "INSERT INTO clusters VALUES (?, ?, ?, ?)",
        [(1, json.dumps([1.0, 0.0]), 5, "10_Knowledge/alpha.md"),
         (2, json.dumps([0.9, 0.1]), 3, "10_Knowledge/beta.md"),
         (3, json.dumps([0.0, 1.0]), 1, None)],
    )
    connection.executemany("INSERT INTO cluster_members VALUES (?, ?, ?)", [("a", 1, "1"), ("b", 2, "2")])
    connection.executemany("INSERT INTO rss_candidates VALUES (?, ?)", [("a", "Alpha"), ("b", "Beta")])
    connection.commit()
    connection.close()

    vectors = {"alpha.md": [1.0, 0.0], "beta.md": [0.9, 0.1]}
    result = build_mocs(vault, database, lambda text: vectors["alpha.md" if "Alpha" in text else "beta.md"])

    assert result == {"mocs": 1, "grouped_pages": 2, "unlinked_pages": 0, "unpromoted_clusters": 1, "embeddings_updated": 2}
    moc = vault / "20_MOC" / "MOC-001.md"
    assert GENERATED_MARKER in moc.read_text(encoding="utf-8")
    connection = sqlite3.connect(database)
    assert connection.execute("SELECT COUNT(*) FROM moc_members").fetchone()[0] == 2
    connection.close()
