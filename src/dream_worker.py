"""Single-job Dreaming worker for extracting reviewed facts and proposing links."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from src.memory_pipeline import process_source_facts
from src.memory_store import MemoryStore


RELATION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "relations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "from_fact_id": {"type": "string"},
                    "to_fact_id": {"type": "string"},
                    "relation_type": {
                        "type": "string",
                        "enum": ["same", "extends", "updates", "contradicts", "derived_from"],
                    },
                    "confidence": {"type": "number"},
                    "rationale": {"type": "string"},
                },
                "required": [
                    "from_fact_id",
                    "to_fact_id",
                    "relation_type",
                    "confidence",
                    "rationale",
                ],
            },
        }
    },
    "required": ["relations"],
}


@dataclass(frozen=True)
class DreamRunResult:
    result: str
    job_id: str | None = None
    status: str | None = None
    attempts: int | None = None
    accepted_fact_ids: tuple[str, ...] = ()
    proposed_relation_ids: tuple[str, ...] = ()
    error: str = ""


@dataclass(frozen=True)
class DreamBatchResult:
    result: str
    processed_count: int
    completed_count: int
    error_count: int
    jobs: tuple[DreamRunResult, ...]


def _propose_relations(
    store: MemoryStore, fact_ids: tuple[str, ...], evaluator: Any
) -> tuple[str, ...]:
    if not fact_ids:
        return ()
    placeholders = ",".join("?" for _ in fact_ids)
    rows = store.connection.execute(
        "SELECT f.fact_id, f.statement, e.quote FROM memory_facts f "
        "LEFT JOIN fact_evidence e ON e.fact_id = f.fact_id "
        f"WHERE f.fact_id IN ({placeholders}) ORDER BY f.recorded_at DESC LIMIT 20",
        fact_ids,
    ).fetchall()
    new_facts = [row for row in rows]
    prior = store.connection.execute(
        "SELECT f.fact_id, f.statement, e.quote FROM memory_facts f "
        "LEFT JOIN fact_evidence e ON e.fact_id = f.fact_id "
        "WHERE f.status = 'active' AND f.fact_id NOT IN (" + placeholders + ") "
        "ORDER BY f.recorded_at DESC LIMIT 20",
        fact_ids,
    ).fetchall()
    candidates = new_facts + prior
    if len(candidates) < 2:
        return ()
    payload = [
        {"fact_id": row[0], "statement": row[1], "evidence_quote": row[2] or ""}
        for row in candidates
    ]
    response = evaluator.chat(
        "Find only clear, specific semantic relations between these atomic facts. Shared topic "
        "alone is not a relation. Use updates when one explicitly changes the earlier claim; "
        "contradicts only when claims cannot both hold for the same scope and time. Return no "
        "relation when uncertain. Return JSON only.",
        json.dumps(payload, ensure_ascii=False),
        RELATION_SCHEMA,
    )
    known = {str(item["fact_id"]) for item in payload}
    fresh = set(fact_ids)
    proposed: list[str] = []
    seen: set[tuple[str, str, str]] = set()
    for item in response.get("relations", []):
        if not isinstance(item, dict):
            continue
        source = str(item.get("from_fact_id", ""))
        target = str(item.get("to_fact_id", ""))
        relation_type = str(item.get("relation_type", ""))
        rationale = str(item.get("rationale", "")).strip()
        try:
            confidence = float(item.get("confidence", 0))
        except (TypeError, ValueError):
            continue
        key = (source, target, relation_type)
        if (
            source not in fresh
            or target not in known
            or source == target
            or not rationale
            or confidence < 0.65
            or key in seen
        ):
            continue
        try:
            result = store.propose_fact_relation(
                source, target, relation_type, confidence=confidence, rationale=rationale
            )
        except ValueError:
            continue
        seen.add(key)
        proposed.append(result.relation_id)
    return tuple(proposed)


def run_dream_once(
    store: MemoryStore,
    worker_id: str,
    *,
    extractor: Any,
    fact_reviewer: Any,
    translator: Any,
    localization_reviewer: Any,
    relation_evaluator: Any,
    retry_only: bool = False,
) -> DreamRunResult:
    job = store.claim_dream_job(worker_id, retry_only=retry_only)
    if job is None:
        return DreamRunResult("idle")
    try:
        source_id = job.payload.get("source_id")
        if not isinstance(source_id, str) or not source_id:
            raise ValueError("Dreaming job has no source_id")
        facts = process_source_facts(
            store,
            source_id,
            extractor=extractor,
            fact_reviewer=fact_reviewer,
            translator=translator,
            localization_reviewer=localization_reviewer,
        )
        relations = _propose_relations(store, facts.accepted_fact_ids, relation_evaluator)
        store.complete_dream_job(job.job_id, worker_id)
        return DreamRunResult(
            "completed",
            job.job_id,
            "succeeded",
            job.attempts,
            facts.accepted_fact_ids,
            relations,
        )
    except Exception as error:  # Keep one job failure isolated and available for retry.
        failed = store.fail_dream_job(job.job_id, worker_id, repr(error))
        return DreamRunResult(
            "error", job.job_id, failed.status, failed.attempts, error=repr(error)
        )


def run_dream_batch(
    store: MemoryStore,
    worker_id: str,
    *,
    extractor: Any,
    fact_reviewer: Any,
    translator: Any,
    localization_reviewer: Any,
    relation_evaluator: Any,
    max_jobs: int = 10,
    retry_only: bool = False,
) -> DreamBatchResult:
    """Process up to max_jobs; a retriable failure does not block other ready jobs."""
    if max_jobs < 1:
        raise ValueError("max_jobs must be positive")
    results: list[DreamRunResult] = []
    for _ in range(max_jobs):
        result = run_dream_once(
            store,
            worker_id,
            extractor=extractor,
            fact_reviewer=fact_reviewer,
            translator=translator,
            localization_reviewer=localization_reviewer,
            relation_evaluator=relation_evaluator,
            retry_only=retry_only,
        )
        if result.result == "idle":
            break
        results.append(result)
    errors = sum(result.result == "error" for result in results)
    completed = sum(result.result == "completed" for result in results)
    status = "idle" if not results else "error" if errors else "completed"
    return DreamBatchResult(status, len(results), completed, errors, tuple(results))
