import json
from pathlib import Path
from typing import Any

import pytest

from src import discord_notify
from src.discord_notify import build_payload, conclusion_excerpt, map_change_line, notify_run

PAGE = """---
title: テスト
type: knowledge
---

# 量子計算の現状

## 0. 結論
量子誤り訂正が実用段階に入りつつある。

## テーマ概要
概要の本文。
"""


def _write_page(root: Path, name: str = "10_Knowledge/量子.md") -> str:
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(PAGE, encoding="utf-8")
    return name


def _stats(clusters: int, members: int, relations: int) -> dict[str, Any]:
    return {"status": "updated", "clusters": clusters, "members": members, "relations": relations}


def test_conclusion_excerpt_takes_the_conclusion_section() -> None:
    assert conclusion_excerpt(PAGE) == "量子誤り訂正が実用段階に入りつつある。"


def test_conclusion_excerpt_accepts_unnumbered_heading_and_truncates() -> None:
    page = "# 題\n\n## 結論\n" + "あ" * 400 + "\n\n## 次\n本文"
    excerpt = conclusion_excerpt(page, limit=300)
    assert excerpt == "あ" * 300 + "…"


def test_conclusion_excerpt_falls_back_to_body_without_conclusion() -> None:
    assert conclusion_excerpt("---\na: b\n---\n\n# 題\n\n本文だけ。\n") == "本文だけ。"


def test_map_change_line_shows_differences() -> None:
    line = map_change_line(_stats(42, 310, 18), {"clusters": 40, "members": 303, "relations": 18})
    assert line == "クラスタ 42 (+2) / 点 310 (+7) / 関係 18 (±0)"


def test_map_change_line_without_previous_values() -> None:
    assert map_change_line(_stats(42, 310, 18), None) == "クラスタ 42 / 点 310 / 関係 18"


def test_map_change_line_reports_failed_map() -> None:
    assert map_change_line({"status": "failed", "error": "x"}, None) == "マップ更新失敗"
    assert map_change_line(None, None) == "マップ更新失敗"


def test_build_payload_uses_page_title_and_conclusion(tmp_path: Path) -> None:
    target = _write_page(tmp_path)
    result = {
        "result": "success",
        "action": {"action": "create_page", "target": target},
        "git_status": "pushed",
        "cluster_visualization": _stats(2, 5, 1),
    }
    payload = build_payload(result, tmp_path, None)
    assert payload["embeds"] == [
        {"title": "量子計算の現状", "description": "量子誤り訂正が実用段階に入りつつある。"}
    ]
    assert "create_page" in payload["content"]
    assert "pushed" in payload["content"]
    assert "クラスタ 2 / 点 5 / 関係 1" in payload["content"]


def test_build_payload_lists_every_new_page(tmp_path: Path) -> None:
    first = _write_page(tmp_path, "10_Knowledge/a.md")
    second = _write_page(tmp_path, "10_Knowledge/b.md")
    result = {
        "result": "expanded",
        "action": {"action": "expand_knowledge"},
        "new_pages": [first, second],
        "git_status": "committed",
    }
    assert len(build_payload(result, tmp_path, None)["embeds"]) == 2


@pytest.mark.parametrize("outcome", ["proposal", "review_rejected", "error", "timeout"])
def test_notify_run_skips_non_report_results(tmp_path: Path, outcome: str) -> None:
    posted: list[Any] = []
    status = notify_run({"result": outcome}, tmp_path, "https://example.invalid/hook", posted.append)
    assert status == {"status": "skipped", "reason": "no_report"}
    assert posted == []


def test_notify_run_skips_without_webhook(tmp_path: Path) -> None:
    posted: list[Any] = []
    status = notify_run({"result": "success"}, tmp_path, "", posted.append)
    assert status == {"status": "skipped", "reason": "no_webhook"}
    assert posted == []


def test_notify_run_posts_and_stores_map_stats(tmp_path: Path) -> None:
    target = _write_page(tmp_path)
    (tmp_path / discord_notify.STATS_FILE).write_text(
        json.dumps({"clusters": 1, "members": 3, "relations": 0}), encoding="utf-8"
    )
    posted: list[Any] = []
    result = {
        "result": "success",
        "action": {"action": "improve_page", "target": target},
        "git_status": "pushed",
        "cluster_visualization": _stats(2, 5, 1),
    }
    status = notify_run(result, tmp_path, "https://example.invalid/hook", posted.append)
    assert status == {"status": "sent"}
    assert "クラスタ 2 (+1) / 点 5 (+2) / 関係 1 (+1)" in posted[0]["content"]
    stored = json.loads((tmp_path / discord_notify.STATS_FILE).read_text(encoding="utf-8"))
    assert stored == {"clusters": 2, "members": 5, "relations": 1}


def test_notify_run_keeps_previous_stats_when_map_failed(tmp_path: Path) -> None:
    target = _write_page(tmp_path)
    previous = {"clusters": 1, "members": 3, "relations": 0}
    (tmp_path / discord_notify.STATS_FILE).write_text(json.dumps(previous), encoding="utf-8")
    result = {
        "result": "success",
        "action": {"action": "improve_page", "target": target},
        "cluster_visualization": {"status": "failed", "error": "x"},
    }
    notify_run(result, tmp_path, "https://example.invalid/hook", lambda _payload: None)
    stored = json.loads((tmp_path / discord_notify.STATS_FILE).read_text(encoding="utf-8"))
    assert stored == previous
