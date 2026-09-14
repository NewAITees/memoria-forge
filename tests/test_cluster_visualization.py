import json
import sqlite3
from pathlib import Path

import pytest

from experiments.visualize_clusters import generate, internal_similarity, nearest_relations


def test_internal_similarity_uses_centroid_length() -> None:
    assert internal_similarity([0.8, 0.0], 2) == pytest.approx(0.28)
    assert internal_similarity([1.0, 0.0], 1) == 0.0


def test_nearest_relations_connects_close_clusters() -> None:
    clusters = [
        {"id": 1, "centroid": [1.0, 0.0]},
        {"id": 2, "centroid": [0.9, 0.1]},
        {"id": 3, "centroid": [0.0, 1.0]},
    ]
    relations = nearest_relations(clusters, minimum=0.8)
    assert [(item["source"], item["target"]) for item in relations] == [(1, 2)]


def test_generate_builds_html_from_database(tmp_path: Path) -> None:
    database = tmp_path / "state.sqlite3"
    connection = sqlite3.connect(database)
    connection.executescript("""
        CREATE TABLE clusters (cluster_id INTEGER, centroid TEXT, size INTEGER, updated_at TEXT, page_path TEXT, paged_size INTEGER);
        CREATE TABLE cluster_members (url TEXT, cluster_id INTEGER, assigned_at TEXT, embedding TEXT);
        CREATE TABLE rss_candidates (url TEXT, title TEXT);
        CREATE TABLE mocs (moc_id INTEGER, title TEXT, page_path TEXT, updated_at TEXT);
        CREATE TABLE moc_members (moc_id INTEGER, page_path TEXT, cluster_id INTEGER, similarity REAL);
    """)
    connection.executemany(
        "INSERT INTO clusters VALUES (?, ?, ?, '', ?, ?)",
        [(1, json.dumps([1.0, 0.0]), 2, "topic.md", 2), (2, json.dumps([0.9, 0.1]), 1, None, None)],
    )
    connection.executemany("INSERT INTO cluster_members VALUES (?, ?, ?, ?)", [("a", 1, "1", "[]"), ("b", 2, "2", "[]")])
    connection.executemany("INSERT INTO rss_candidates VALUES (?, ?)", [("a", "Alpha"), ("b", "Beta")])
    connection.execute("INSERT INTO mocs VALUES (1, 'MOC — Alpha', '20_MOC/MOC-001.md', '')")
    connection.execute("INSERT INTO moc_members VALUES (1, 'topic.md', 1, 0.9)")
    connection.commit()
    connection.close()

    output = tmp_path / "map.html"
    assert generate(database, output)["clusters"] == 2
    rendered = output.read_text(encoding="utf-8")
    assert "クラスタ分布マップ" in rendered
    assert "Alpha" in rendered
    assert '"members":["Alpha"]' in rendered
    assert '"moc_title":"MOC — Alpha"' in rendered
    assert "<!doctype html>" in rendered
