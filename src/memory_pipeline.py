"""Reviewed fact extraction pipeline for the independent local memory store."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from src.atomic_facts import (
    AtomicFact,
    extract_verified_facts,
    filter_reviewed_facts,
    localize_verified_facts,
    review_facts,
)
from src.memory_store import MemoryStore


@dataclass(frozen=True)
class _SourceMaterial:
    title: str
    url: str
    snippet: str


@dataclass(frozen=True)
class MemoryPipelineResult:
    accepted_fact_ids: tuple[str, ...]
    rejected: dict[str, str]
    localized_fact_ids: tuple[str, ...]


@dataclass(frozen=True)
class PersistedMemoryResult:
    ingested_source_count: int
    persisted_fact_count: int
    fact_ids: tuple[str, ...]
    skipped: dict[str, str]


def process_source_facts(
    store: MemoryStore,
    source_id: str,
    *,
    extractor: Any,
    fact_reviewer: Any,
    translator: Any,
    localization_reviewer: Any,
) -> MemoryPipelineResult:
    """Extract, review, and persist facts without publishing unreviewed model output."""
    source = store.connection.execute(
        "SELECT title, source_uri, raw_content, source_state FROM source_documents "
        "WHERE source_id = ?",
        (source_id,),
    ).fetchone()
    if source is None or source[3] != "active":
        raise ValueError("source is missing or inactive")

    material = _SourceMaterial(str(source[0]), str(source[1]), str(source[2]))
    candidates, rejected = extract_verified_facts(
        extractor,
        material.title or material.url,
        material.snippet,
        [material],
    )
    review = (
        review_facts(fact_reviewer, candidates)
        if candidates
        else {"accepted_fact_ids": [], "rejected": []}
    )
    accepted, fact_rejections = filter_reviewed_facts(candidates, review)
    rejected.update(fact_rejections)

    stored_ids: dict[str, str] = {}
    persisted_rejections: dict[str, str] = {}
    persisted_active_facts: list[AtomicFact] = []
    for fact in candidates:
        stored = store.add_fact_candidate(
            source_id,
            fact.statement,
            fact.evidence_quote,
            language=_language_of(fact.statement),
            confidence=fact.confidence,
        )
        stored_ids[fact.fact_id] = stored.fact_id
        if fact.fact_id in fact_rejections:
            rejected.pop(fact.fact_id, None)
        current_status = store.connection.execute(
            "SELECT status FROM memory_facts WHERE fact_id = ?", (stored.fact_id,)
        ).fetchone()[0]
        if current_status == "pending_review":
            is_accepted = fact in accepted
            reason = "" if is_accepted else fact_rejections.get(fact.fact_id, "reviewer_rejected")
            store.review_fact(
                stored.fact_id,
                accepted=is_accepted,
                reviewer=type(fact_reviewer).__name__,
                reason=reason,
            )
            if not is_accepted:
                persisted_rejections[stored.fact_id] = reason
            current_status = "active" if is_accepted else "rejected"
        if current_status == "active":
            persisted_active_facts.append(fact)
        else:
            persisted_rejections[stored.fact_id] = fact_rejections.get(
                fact.fact_id, "fact_already_rejected"
            )

    localized, localization_rejections = localize_verified_facts(
        translator, localization_reviewer, persisted_active_facts
    )
    rejected.update(localization_rejections)
    rejected.update(persisted_rejections)
    localized_ids: list[str] = []
    for fact in localized:
        stored_id = stored_ids[fact.fact_id]
        if _language_of(fact.statement) == "ja":
            # The source claim is already Japanese, so the claim itself is the display text.
            continue
        existing = store.connection.execute(
            "SELECT review_status FROM memory_localizations WHERE fact_id = ? AND locale = 'ja'",
            (stored_id,),
        ).fetchone()
        if existing is not None:
            if existing[0] == "approved":
                localized_ids.append(stored_id)
            continue
        store.save_localization(stored_id, "ja", fact.statement_ja)
        store.review_localization(
            stored_id,
            "ja",
            approved=True,
            reviewer=type(localization_reviewer).__name__,
        )
        localized_ids.append(stored_id)

    return MemoryPipelineResult(
        accepted_fact_ids=tuple(stored_ids[fact.fact_id] for fact in persisted_active_facts),
        rejected=rejected,
        localized_fact_ids=tuple(localized_ids),
    )


def persist_reviewed_facts(
    store: MemoryStore, sources: list[Any], facts: list[AtomicFact]
) -> PersistedMemoryResult:
    """Persist excerpts and facts already accepted by the Wiki quality pipeline."""
    source_ids: dict[str, str] = {}
    ingested_source_count = 0
    for source in sources:
        url = str(getattr(source, "url", "")).strip()
        snippet = str(getattr(source, "snippet", "")).strip()
        if not url or not snippet:
            continue
        stored_source = store.add_source(
            url,
            snippet,
            title=str(getattr(source, "title", "")),
            media_type="text/x-web-excerpt",
        )
        source_ids[url] = stored_source.source_id
        ingested_source_count += int(stored_source.created)

    fact_ids: list[str] = []
    skipped: dict[str, str] = {}
    for fact in facts:
        source_id = source_ids.get(fact.source_url)
        if source_id is None:
            skipped[fact.fact_id] = "source_excerpt_not_available"
            continue
        try:
            stored_fact = store.add_fact_candidate(
                source_id,
                fact.statement,
                fact.evidence_quote,
                language=_language_of(fact.statement),
                confidence=fact.confidence,
            )
        except ValueError as error:
            skipped[fact.fact_id] = str(error)
            continue

        status = store.connection.execute(
            "SELECT status FROM memory_facts WHERE fact_id = ?", (stored_fact.fact_id,)
        ).fetchone()[0]
        if status == "pending_review":
            store.review_fact(
                stored_fact.fact_id,
                accepted=True,
                reviewer="wiki_fact_quality_gate",
                reason="Passed extraction, evidence, implication, and localization review.",
            )
            status = "active"
        if status != "active":
            skipped[fact.fact_id] = f"stored_fact_status:{status}"
            continue

        if _language_of(fact.statement) != "ja" and fact.statement_ja.strip():
            localization = store.connection.execute(
                "SELECT review_status FROM memory_localizations "
                "WHERE fact_id = ? AND locale = 'ja'",
                (stored_fact.fact_id,),
            ).fetchone()
            if localization is None:
                store.save_localization(stored_fact.fact_id, "ja", fact.statement_ja)
                store.review_localization(
                    stored_fact.fact_id,
                    "ja",
                    approved=True,
                    reviewer="wiki_localization_quality_gate",
                    reason="Passed translation review before page approval.",
                )
            elif localization[0] != "approved":
                skipped[fact.fact_id] = "localization_not_approved"
                continue
        fact_ids.append(stored_fact.fact_id)

    return PersistedMemoryResult(
        ingested_source_count=ingested_source_count,
        persisted_fact_count=len(fact_ids),
        fact_ids=tuple(fact_ids),
        skipped=skipped,
    )


def _language_of(statement: str) -> str:
    return "ja" if re.search(r"[\u3040-\u30ff\u3400-\u9fff]", statement) else "en"
