"""Second shadow experiment with evidence review and bounded relation candidates."""

from __future__ import annotations

import argparse
import json
import sqlite3
import time
from pathlib import Path
from typing import Any

from experiments.atomic_fact_graph import (
    Fact,
    SourceDocument,
    candidate_relation_pairs,
    unsupported_critical_tokens,
)
from experiments.run_atomic_fact_experiment import render_page
from src.wiki_agent import Ollama


ENTAILMENT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "accepted_fact_ids": {"type": "array", "items": {"type": "string"}},
        "rejected": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "fact_id": {"type": "string"},
                    "reason": {"type": "string"},
                },
                "required": ["fact_id", "reason"],
            },
        },
    },
    "required": ["accepted_fact_ids", "rejected"],
}

BOUNDED_RELATION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "relations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "left_id": {"type": "string"},
                    "right_id": {"type": "string"},
                    "relation": {
                        "type": "string",
                        "enum": ["same", "updates", "contradicts"],
                    },
                    "reason": {"type": "string"},
                },
                "required": ["left_id", "right_id", "relation", "reason"],
            },
        }
    },
    "required": ["relations"],
}


def load_previous(database: Path) -> tuple[list[Fact], dict[str, SourceDocument]]:
    connection = sqlite3.connect(f"file:{database.as_posix()}?mode=ro", uri=True)
    facts = [
        Fact(*row)
        for row in connection.execute(
            "SELECT fact_id, statement, evidence_quote, source_document_id, confidence, status "
            "FROM facts ORDER BY fact_id"
        ).fetchall()
    ]
    sources = {
        row[0]: SourceDocument(*row)
        for row in connection.execute(
            "SELECT document_id, title, url, content FROM documents"
        ).fetchall()
    }
    connection.close()
    return facts, sources


def semantic_review(client: Ollama, facts: list[Fact]) -> dict[str, Any]:
    payload = [
        {
            "fact_id": fact.fact_id,
            "claim": fact.statement,
            "quote": fact.evidence_quote,
        }
        for fact in facts
    ]
    return client.chat(
        "You are an evidence reviewer, separate from the fact writer. Accept a claim only when its "
        "quoted text alone supports every condition, number, entity, and causal qualification in the "
        "claim. Reject embellishment even if it may appear elsewhere in the source. Return JSON only.",
        json.dumps(payload, ensure_ascii=False),
        ENTAILMENT_SCHEMA,
    )


def review_relations(client: Ollama, pairs: list[tuple[Fact, Fact]]) -> dict[str, Any]:
    payload = [
        {
            "left_id": left.fact_id,
            "left": left.statement,
            "right_id": right.fact_id,
            "right": right.statement,
        }
        for left, right in pairs
    ]
    return client.chat(
        "Review only the supplied candidate pairs. Emit a relation only if both facts describe the "
        "same real-world subject and attribute: same means equivalent, updates means a newer state "
        "replaces an older state, contradicts means they cannot both be true in the same scope and "
        "time. Related topic, compatible detail, or shared technology is no relation. Return JSON only.",
        json.dumps(payload, ensure_ascii=False),
        BOUNDED_RELATION_SCHEMA,
    )


def run(args: argparse.Namespace) -> dict[str, Any]:
    started = time.perf_counter()
    args.output.mkdir(parents=True, exist_ok=True)
    facts, sources = load_previous(args.database)

    deterministic_rejected: dict[str, list[str]] = {}
    deterministic_accepted: list[Fact] = []
    for fact in facts:
        unsupported = sorted(unsupported_critical_tokens(fact.statement, fact.evidence_quote))
        if unsupported:
            deterministic_rejected[fact.fact_id] = unsupported
        else:
            deterministic_accepted.append(fact)

    reviewer = Ollama(args.ollama_url, args.review_model, timeout=None, num_ctx=16384)
    entailment = semantic_review(reviewer, deterministic_accepted)
    valid_ids = {fact.fact_id for fact in deterministic_accepted}
    semantically_accepted_ids = set(entailment.get("accepted_fact_ids", [])) & valid_ids
    reported_rejected_ids = {
        item.get("fact_id")
        for item in entailment.get("rejected", [])
        if isinstance(item, dict)
    }
    omitted_ids = sorted(valid_ids - semantically_accepted_ids - reported_rejected_ids)
    accepted = [fact for fact in deterministic_accepted if fact.fact_id in semantically_accepted_ids]

    pairs = candidate_relation_pairs(accepted)
    relation_review = review_relations(reviewer, pairs)
    pair_ids = {(left.fact_id, right.fact_id) for left, right in pairs}
    relations = [
        relation
        for relation in relation_review.get("relations", [])
        if isinstance(relation, dict)
        and (relation.get("left_id"), relation.get("right_id")) in pair_ids
    ]

    previous = json.loads(args.previous_result.read_text(encoding="utf-8"))
    previously_selected = {
        item["fact_id"] for item in previous.get("selected_facts", []) if isinstance(item, dict)
    }
    page_facts = [fact for fact in accepted if fact.fact_id in previously_selected]
    (args.output / "fact-grounded-page-v2.md").write_text(
        render_page(args.target, page_facts, sources), encoding="utf-8", newline="\n"
    )

    result = {
        "input_fact_count": len(facts),
        "deterministic_accepted_count": len(deterministic_accepted),
        "deterministic_rejected": deterministic_rejected,
        "semantic_accepted_count": len(accepted),
        "semantic_rejected": entailment.get("rejected", [])
        + [{"fact_id": fact_id, "reason": "reviewer_omitted_fact"} for fact_id in omitted_ids],
        "relation_candidate_count": len(pairs),
        "accepted_relation_count": len(relations),
        "relations": relations,
        "page_fact_count": len(page_facts),
        "elapsed_seconds": round(time.perf_counter() - started, 2),
        "comparison": {
            "v1_relations": 103,
            "v2_relations": len(relations),
            "v1_page_facts": 8,
            "v2_page_facts": len(page_facts),
        },
    }
    (args.output / "result-v2.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--database",
        type=Path,
        default=Path("experiments/atomic_fact_result/atomic-facts.sqlite3"),
    )
    parser.add_argument(
        "--previous-result",
        type=Path,
        default=Path("experiments/atomic_fact_result/result.json"),
    )
    parser.add_argument(
        "--target", default="Kubernetes HPA on Amazon EKS: Scaling from 2 to 6 Pods Under Load"
    )
    parser.add_argument("--ollama-url", default="http://localhost:11434")
    parser.add_argument("--review-model", default="gemma3:4b")
    parser.add_argument("--output", type=Path, default=Path("experiments/atomic_fact_result"))
    args = parser.parse_args()
    print(json.dumps(run(args), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
