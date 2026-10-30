"""Exercise the production grounded-page path against a copied live database."""

from __future__ import annotations

import argparse
import json
import sqlite3
import shutil
from pathlib import Path

from src.atomic_facts import store_page_facts
from src.wiki_agent import (
    Config,
    StateDB,
    build_cluster_context,
    create_client,
    create_reviewer_client,
    format_deep_research,
    now,
    SearchResult,
    write_grounded_and_review,
)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("config.json"))
    parser.add_argument("--cluster-id", type=int, default=1718)
    parser.add_argument("--source-url", default="")
    parser.add_argument(
        "--target",
        type=Path,
        default=Path("10_Knowledge/Kubernetes HPA on Amazon EKS.md"),
    )
    parser.add_argument(
        "--output", type=Path, default=Path("experiments/grounded_pipeline_result")
    )
    args = parser.parse_args()

    config = Config.load(args.config)
    source_database = config.vault_path / ".agent-state.sqlite3"
    args.output.mkdir(parents=True, exist_ok=True)
    copied_database = args.output / "state.sqlite3"
    shutil.copy2(source_database, copied_database)
    db = StateDB(copied_database)
    writer = create_client(config)
    reviewer = create_reviewer_client(config)
    if args.source_url:
        connection = sqlite3.connect(f"file:{copied_database.as_posix()}?mode=ro", uri=True)
        row = connection.execute(
            "SELECT title, content FROM rss_candidates WHERE url = ?", (args.source_url,)
        ).fetchone()
        research_row = connection.execute(
            "SELECT results, synthesis FROM deep_research WHERE rss_url = ?",
            (args.source_url,),
        ).fetchone()
        connection.close()
        if row is None:
            raise ValueError(f"source URL not found in copied database: {args.source_url}")
        if research_row:
            research = {
                "results": json.loads(research_row[0] or "[]"),
                "synthesis": research_row[1] or "",
            }
            context, sources = format_deep_research(research)
        else:
            context = ""
            sources = []
        if not sources:
            sources = [SearchResult(str(row[0]), args.source_url, str(row[1]))]
        searches = 0
    else:
        context, sources, searches = build_cluster_context(db, writer, args.cluster_id, config)
    accepted, page, review, facts = write_grounded_and_review(
        writer,
        reviewer,
        args.target,
        sources,
        context,
        args.output,
    )
    if accepted:
        page_path = args.output / "grounded-page.md"
        page_path.write_text(page, encoding="utf-8", newline="\n")
        store_page_facts(db.db, args.target.as_posix(), facts, now())
    result = {
        "accepted": accepted,
        "cluster_id": args.cluster_id,
        "source_count": len(sources),
        "new_searches": searches,
        "verified_fact_count": len(facts),
        "review": review,
    }
    (args.output / "result.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
