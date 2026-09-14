"""Post a Discord message when an agent run produces a Wiki page (the "report").

Related: run_agent._run_once_worker (caller), experiments/visualize_clusters.generate
(map stats), src.wiki_agent.push_pending (git_final), tasks/alignment.md
"Discord通知 / Discord Notification".
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from pathlib import Path
from typing import Any
from urllib.parse import quote

import requests  # type: ignore[import-untyped]

REPORT_RESULTS = ("success", "expanded")
STATS_FILE = ".cluster-map-stats.json"
STATS_KEYS = (("clusters", "クラスタ"), ("members", "点"), ("relations", "関係"))
EXCERPT_CHARS = 300
REPO_BLOB_URL = "https://github.com/NewAITees/memoria-forge/blob/master/"


def read_webhook_url(path: Path) -> str:
    """Return the first line of the git-ignored webhook file; empty disables notices."""
    if not path.exists():
        return ""
    lines = path.read_text(encoding="utf-8").splitlines()
    return lines[0].strip() if lines else ""


def conclusion_excerpt(page: str, limit: int = EXCERPT_CHARS) -> str:
    """Return the conclusion section, or the body under the H1 when there is none."""
    body = re.sub(r"^---\n.*?\n---\n", "", page, flags=re.DOTALL)
    match = re.search(r"(?m)^##\s*(?:\d+\.\s*)?結論\s*\n(.*?)(?=^##\s|\Z)", body, re.DOTALL)
    text = match.group(1) if match else re.sub(r"(?m)^#\s+.*$", "", body)
    text = text.strip()
    return text[:limit] + "…" if len(text) > limit else text


def map_change_line(current: dict[str, Any] | None, previous: dict[str, Any] | None) -> str:
    if not current or current.get("status") != "updated":
        return "マップ更新失敗"
    parts = []
    for key, label in STATS_KEYS:
        value = int(current[key])
        if previous is None:
            parts.append(f"{label} {value}")
            continue
        delta = value - int(previous[key])
        parts.append(f"{label} {value} ({f'{delta:+d}' if delta else '±0'})")
    return " / ".join(parts)


def _page_title(page: str, fallback: str) -> str:
    heading = re.search(r"(?m)^#\s+(.+)$", page)
    return heading.group(1).strip() if heading else fallback


def build_payload(
    result: dict[str, Any], vault_root: Path, previous: dict[str, Any] | None
) -> dict[str, Any]:
    action = result.get("action", {})
    git = result.get("git_final", {})
    git_status = git.get("status", "?")
    targets = result.get("new_pages") or [action["target"]]
    embeds = []
    for target in targets[:10]:
        relative = Path(target.replace("\\", "/"))
        path = relative if relative.is_absolute() else vault_root / relative
        page = path.read_text(encoding="utf-8")
        embed = {"title": _page_title(page, path.stem)[:256], "description": conclusion_excerpt(page)}
        if git_status == "pushed":
            # Link only once the page is really on GitHub; before that it would 404.
            repo_path = f"{vault_root.name}/{path.relative_to(vault_root).as_posix()}"
            embed["url"] = REPO_BLOB_URL + quote(repo_path)
        embeds.append(embed)
    git_line = (
        f"⚠️ push失敗: {str(git.get('error', ''))[:300]}"
        if git_status in ("push_failed", "failed")
        else f"Git: {git_status}"
    )
    content = (
        f"@everyone 📝 レポート生成: {action.get('action', '?')} / {git_line}\n"
        f"🗺️ {map_change_line(result.get('cluster_visualization'), previous)}"
    )
    return {"content": content, "embeds": embeds, "allowed_mentions": {"parse": ["everyone"]}}


def _post(webhook_url: str) -> Callable[[dict[str, Any]], None]:
    def send(payload: dict[str, Any]) -> None:
        requests.post(webhook_url, json=payload, timeout=10).raise_for_status()

    return send


def notify_run(
    result: dict[str, Any],
    vault_root: Path,
    webhook_url: str,
    send: Callable[[dict[str, Any]], None] | None = None,
) -> dict[str, str]:
    """Send the report notification and remember the map stats it was compared with."""
    if result.get("result") not in REPORT_RESULTS:
        return {"status": "skipped", "reason": "no_report"}
    if not webhook_url:
        return {"status": "skipped", "reason": "no_webhook"}
    stats_path = vault_root / STATS_FILE
    previous = (
        json.loads(stats_path.read_text(encoding="utf-8")) if stats_path.exists() else None
    )
    (send or _post(webhook_url))(build_payload(result, vault_root, previous))
    current = result.get("cluster_visualization")
    if current and current.get("status") == "updated":
        stats_path.write_text(
            json.dumps({key: current[key] for key, _ in STATS_KEYS}), encoding="utf-8"
        )
    return {"status": "sent"}
