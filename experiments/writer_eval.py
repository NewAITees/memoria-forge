"""Measure the Writer on N page-eligible clusters with the production pipeline.

Run before shipping any prompt or page-format change: a single passing example is
not evidence (a change verified on one sample once left every run rejected for four
weeks). Nothing touches the vault, Git, or the live state DB -- the DB is copied with
SQLite's backup API and rejected drafts land in the same temporary folder.

Related: src.wiki_agent.write_and_review (the shared loop), geometry_menu,
build_cluster_context.
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
import tempfile
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.wiki_agent import (
    Config,
    StateDB,
    Vault,
    build_cluster_context,
    create_client,
    create_reviewer_client,
    geometry_menu,
    safe_new_page_target,
    write_and_review,
)


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    reasons: Counter[str] = Counter()
    for result in results:
        if not result["accepted"]:
            reasons.update(part for part in str(result["reason"]).split("; ") if part)
    return {
        "total": len(results),
        "passed": sum(1 for result in results if result["accepted"]),
        "reasons": dict(reasons.most_common()),
    }


def count_truncations(log_text: str, since: str) -> int:
    """Count Ollama prompt truncations at or after an ISO timestamp."""
    cutoff = datetime.fromisoformat(since)
    count = 0
    for line in log_text.splitlines():
        if 'msg="truncating input prompt"' not in line:
            continue
        timestamp = next(
            (part.removeprefix("time=") for part in line.split() if part.startswith("time=")),
            None,
        )
        if timestamp is not None and datetime.fromisoformat(timestamp) >= cutoff:
            count += 1
    return count


def _review_reason(review: dict[str, Any]) -> str:
    issues = review.get("issues", [])
    return "; ".join(
        str(issue.get("description", "")) if isinstance(issue, dict) else str(issue)
        for issue in issues
    )


def evaluate(config: Config, count: int) -> tuple[list[dict[str, Any]], Path]:
    workdir = Path(tempfile.mkdtemp(prefix="writer-eval-"))
    live = sqlite3.connect((config.vault_path / ".agent-state.sqlite3").resolve().as_uri() + "?mode=ro", uri=True)
    copy = sqlite3.connect(workdir / "state.sqlite3")
    live.backup(copy)
    live.close()
    copy.close()
    db = StateDB(workdir / "state.sqlite3")
    vault = Vault(config.vault_path)
    client = create_client(config)
    reviewer = create_reviewer_client(config)
    results: list[dict[str, Any]] = []
    for action in geometry_menu(vault, db, config)[:count]:
        target = Path(action["target"])
        if action["action"] == "create_page" and not vault.safe(target).exists():
            target = safe_new_page_target(target)
        context, sources, _ = build_cluster_context(db, client, int(action["cluster_id"]), config)
        unique = list({source.url: source for source in sources}.values())[: config.max_pages_fetched]
        existing = vault.read(target) if vault.safe(target).exists() else ""
        started = time.monotonic()
        accepted, content, review = write_and_review(
            client, reviewer, target, action["reason"], unique, existing, context, workdir / "vault"
        )
        if accepted:
            accepted_dir = workdir / "accepted"
            accepted_dir.mkdir(exist_ok=True)
            (accepted_dir / f"{target.stem}.md").write_text(content, encoding="utf-8")
        results.append(
            {
                "target": str(target),
                "action": action["action"],
                "sources": len(unique),
                "accepted": accepted,
                "seconds": round(time.monotonic() - started),
                "reason": "" if accepted else _review_reason(review),
            }
        )
        print(json.dumps(results[-1], ensure_ascii=False), flush=True)
    return results, workdir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config.json"))
    parser.add_argument("--count", type=int, default=5)
    args = parser.parse_args()
    started_at = datetime.now(timezone.utc).isoformat()
    results, workdir = evaluate(Config.load(args.config), args.count)
    summary = summarize(results)
    local_app_data = os.environ.get("LOCALAPPDATA")
    log_path = Path(local_app_data) / "Ollama" / "server.log" if local_app_data else None
    if log_path is not None and log_path.exists():
        summary["truncations"] = count_truncations(
            log_path.read_text(encoding="utf-8", errors="replace"), started_at
        )
    else:
        summary["truncations"] = 0
        summary["truncations_note"] = "Ollama server.log not found"
    (workdir / "report.json").write_text(
        json.dumps({"summary": summary, "results": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"summary": summary, "workdir": str(workdir)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
