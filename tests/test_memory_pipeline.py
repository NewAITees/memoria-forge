import re
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from src.atomic_facts import AtomicFact
from src.memory_pipeline import persist_reviewed_facts, process_source_facts
from src.memory_store import MemoryStore


class _Extractor:
    def chat(self, system: str, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        return {
            "facts": [
                {
                    "statement": "The Horizontal Pod Autoscaler scales from 2 to 6 replicas.",
                    "evidence_quote": "The Horizontal Pod Autoscaler scales from 2 to 6 replicas.",
                    "source_id": "source-1",
                    "confidence": 0.91,
                }
            ]
        }


class _Reviewer:
    def __init__(self, accept: bool = True) -> None:
        self.accept = accept

    def chat(self, system: str, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        ids = re.findall(r'"fact_id":\s*"([^"]+)"', prompt)
        if "accepted_fact_ids" in schema.get("properties", {}):
            return {
                "accepted_fact_ids": ids if self.accept else [],
                "rejected": []
                if self.accept
                else [{"fact_id": fact_id, "reason": "unsupported implication"} for fact_id in ids],
            }
        if "translations" in schema.get("properties", {}):
            return {
                "translations": [
                    {
                        "fact_id": fact_id,
                        "statement_ja": "Horizontal Pod Autoscalerは2から6レプリカへ拡張する。",
                    }
                    for fact_id in ids
                ]
            }
        raise AssertionError("unexpected schema")


def test_pipeline_persists_only_reviewed_facts_and_approved_localization(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source = store.add_source(
            "note://hpa",
            "The Horizontal Pod Autoscaler scales from 2 to 6 replicas.",
            title="HPA configuration",
        )
        result = process_source_facts(
            store,
            source.source_id,
            extractor=_Extractor(),
            fact_reviewer=_Reviewer(),
            translator=_Reviewer(),
            localization_reviewer=_Reviewer(),
        )

        assert len(result.accepted_fact_ids) == 1
        assert len(result.localized_fact_ids) == 1
        assert store.get_recall_statement(result.accepted_fact_ids[0], "ja") == (
            "Horizontal Pod Autoscalerは2から6レプリカへ拡張する。"
        )
        assert store.get_recall_statement(result.accepted_fact_ids[0], "en").startswith(
            "The Horizontal Pod Autoscaler"
        )
        repeated = process_source_facts(
            store,
            source.source_id,
            extractor=_Extractor(),
            fact_reviewer=_Reviewer(),
            translator=_Reviewer(),
            localization_reviewer=_Reviewer(),
        )
        assert repeated.accepted_fact_ids == result.accepted_fact_ids
        assert (
            store.connection.execute(
                "SELECT COUNT(*) FROM memory_localizations WHERE fact_id = ?",
                (result.accepted_fact_ids[0],),
            ).fetchone()[0]
            == 1
        )


def test_pipeline_rejects_fact_when_independent_review_rejects_it(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source = store.add_source(
            "note://hpa",
            "The Horizontal Pod Autoscaler scales from 2 to 6 replicas.",
        )
        result = process_source_facts(
            store,
            source.source_id,
            extractor=_Extractor(),
            fact_reviewer=_Reviewer(accept=False),
            translator=_Reviewer(),
            localization_reviewer=_Reviewer(),
        )

        assert result.accepted_fact_ids == ()
        assert result.rejected
        assert (
            store.connection.execute(
                "SELECT status FROM memory_facts WHERE fact_id = ?",
                (next(iter(result.rejected)),),
            ).fetchone()[0]
            == "rejected"
        )


def test_pipeline_canonicalizes_quote_to_the_exact_source_span(tmp_path: Path) -> None:
    class NonVerbatimExtractor:
        def chat(self, system: str, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
            return {
                "facts": [
                    {
                        "statement": "The target is 6 replicas.",
                        "evidence_quote": "The target is 6 replicas.",
                        "source_id": "source-1",
                        "confidence": 0.9,
                    }
                ]
            }

    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source = store.add_source("note://spacing", "The target is  6 replicas.", title="Spacing")

        result = process_source_facts(
            store,
            source.source_id,
            extractor=NonVerbatimExtractor(),
            fact_reviewer=_Reviewer(),
            translator=_Reviewer(),
            localization_reviewer=_Reviewer(),
        )

        assert len(result.accepted_fact_ids) == 1
        evidence = store.connection.execute(
            "SELECT e.quote, d.raw_content FROM fact_evidence e "
            "JOIN source_documents d ON d.source_id = e.source_id WHERE e.fact_id = ?",
            (result.accepted_fact_ids[0],),
        ).fetchone()
        assert evidence == ("The target is  6 replicas.", "The target is  6 replicas.")


def test_persists_already_reviewed_facts_with_explicit_excerpt_source(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source_text = "The Horizontal Pod Autoscaler scales from 2 to 6 replicas."
        fact = AtomicFact(
            fact_id="verified-1",
            statement="The Horizontal Pod Autoscaler scales from 2 to 6 replicas.",
            evidence_quote=source_text,
            source_url="https://example.test/hpa",
            source_title="HPA",
            confidence=0.9,
            statement_ja="Horizontal Pod Autoscalerは2から6レプリカへ拡張する。",
        )
        result = persist_reviewed_facts(
            store,
            [SimpleNamespace(url=fact.source_url, title="HPA", snippet=source_text)],
            [fact],
        )

        assert result.persisted_fact_count == 1
        assert result.ingested_source_count == 1
        fact_id = result.fact_ids[0]
        assert store.get_recall_statement(fact_id, "ja") == fact.statement_ja
        assert (
            store.connection.execute(
                "SELECT media_type FROM source_documents WHERE source_uri = ?",
                (fact.source_url,),
            ).fetchone()[0]
            == "text/x-web-excerpt"
        )
        repeated = persist_reviewed_facts(
            store,
            [SimpleNamespace(url=fact.source_url, title="HPA", snippet=source_text)],
            [fact],
        )
        assert repeated.fact_ids == result.fact_ids
        assert (
            store.connection.execute(
                "SELECT COUNT(*) FROM memory_facts WHERE fact_id = ?", (fact_id,)
            ).fetchone()[0]
            == 1
        )
