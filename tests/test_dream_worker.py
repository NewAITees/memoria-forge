from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.dream_worker import run_dream_batch, run_dream_once
from src.memory_store import MemoryStore


class FakeClient:
    def __init__(self, mode: str = "success", fail_on_uri: str | None = None) -> None:
        self.mode = mode
        self.fail_on_uri = fail_on_uri
        self.calls = 0

    def chat(self, system: str, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
        self.calls += 1
        if "Extract only atomic facts" in system:
            lines = prompt.splitlines()
            source_index = next(
                index for index, line in enumerate(lines) if line.startswith("SOURCE ID: ")
            )
            source_id = lines[source_index].removeprefix("SOURCE ID: ")
            source_url = lines[source_index + 2].removeprefix("SOURCE URL: ")
            if self.mode == "error" or source_url == self.fail_on_uri:
                raise RuntimeError("temporary extraction outage")
            return {
                "facts": [
                    {
                        "statement": "The service uses SQLite.",
                        "evidence_quote": "The service uses SQLite for its local store.",
                        "source_id": source_id,
                        "confidence": 0.9,
                    }
                ]
            }
        if "Review each fact independently" in system:
            payload = json.loads(prompt)
            return {"accepted_fact_ids": [item["fact_id"] for item in payload], "rejected": []}
        if "Translate each verified factual statement" in system:
            payload = json.loads(prompt)
            return {
                "translations": [
                    {"fact_id": item["fact_id"], "statement_ja": "サービスはSQLiteを使用する。"}
                    for item in payload
                ]
            }
        if "Review each Japanese display statement" in system:
            payload = json.loads(prompt)
            return {"accepted_fact_ids": [item["fact_id"] for item in payload], "rejected": []}
        if "Find only clear, specific semantic relations" in system:
            payload = json.loads(prompt)
            return {
                "relations": [
                    {
                        "from_fact_id": payload[0]["fact_id"],
                        "to_fact_id": payload[1]["fact_id"],
                        "relation_type": "updates",
                        "confidence": 0.91,
                        "rationale": "The newer statement explicitly revises the storage choice.",
                    }
                ]
                if self.mode == "success" and len(payload) > 1
                else []
            }
        raise AssertionError(f"unexpected model call: {system[:80]}")


def seed_old_fact(store: MemoryStore) -> str:
    source = store.add_source("note://old", "The service used PostgreSQL.")
    fact = store.add_fact_candidate(
        source.source_id,
        "The service used PostgreSQL.",
        "The service used PostgreSQL.",
        language="en",
    )
    store.review_fact(fact.fact_id, accepted=True, reviewer="test")
    store.save_localization(fact.fact_id, "ja", "サービスはPostgreSQLを使用していた。")
    store.review_localization(fact.fact_id, "ja", approved=True, reviewer="test")
    return fact.fact_id


def test_dream_once_reviews_facts_and_only_proposes_clear_relations(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        old_id = seed_old_fact(store)
        old_job = store.claim_dream_job("seed-worker")
        assert old_job is not None
        store.complete_dream_job(old_job.job_id, "seed-worker")
        store.add_source("note://new", "The service uses SQLite for its local store.")
        writer = FakeClient()
        reviewer = FakeClient()

        result = run_dream_once(
            store,
            "worker-a",
            extractor=writer,
            fact_reviewer=reviewer,
            translator=writer,
            localization_reviewer=reviewer,
            relation_evaluator=reviewer,
        )

        assert result.result == "completed"
        assert len(result.accepted_fact_ids) == 1
        assert len(result.proposed_relation_ids) == 1
        relation = store.connection.execute(
            "SELECT from_fact_id, to_fact_id, relation_type, status FROM fact_relations"
        ).fetchone()
        assert relation == (result.accepted_fact_ids[0], old_id, "updates", "proposed")
        assert (
            store.connection.execute(
                "SELECT status FROM dream_jobs WHERE job_id = ?", (result.job_id,)
            ).fetchone()[0]
            == "succeeded"
        )


def test_dream_once_records_transient_error_for_retry(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        store.add_source("note://new", "The service uses SQLite for its local store.")
        client = FakeClient("error")
        result = run_dream_once(
            store,
            "worker-a",
            extractor=client,
            fact_reviewer=client,
            translator=client,
            localization_reviewer=client,
            relation_evaluator=client,
        )
        assert result.result == "error"
        assert result.status == "retry"
        row = store.connection.execute(
            "SELECT status, attempts, last_error FROM dream_jobs WHERE job_id = ?",
            (result.job_id,),
        ).fetchone()
        assert row == ("retry", 1, "RuntimeError('temporary extraction outage')")


def test_dream_once_completes_when_unmatched_quote_is_rejected(tmp_path: Path) -> None:
    class NonVerbatimExtractor:
        def chat(self, system: str, prompt: str, schema: dict[str, Any]) -> dict[str, Any]:
            return {
                "facts": [
                    {
                        "statement": "The service uses PostgreSQL.",
                        "evidence_quote": "The service uses PostgreSQL for its local store.",
                        "source_id": "source-1",
                        "confidence": 0.9,
                    }
                ]
            }

    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        store.add_source("note://spacing", "The service uses SQLite  for its local store.")
        client = FakeClient()

        result = run_dream_once(
            store,
            "worker-a",
            extractor=NonVerbatimExtractor(),
            fact_reviewer=client,
            translator=client,
            localization_reviewer=client,
            relation_evaluator=client,
        )

        assert result.result == "completed"
        assert result.accepted_fact_ids == ()
        assert (
            store.connection.execute(
                "SELECT status FROM dream_jobs WHERE job_id = ?", (result.job_id,)
            ).fetchone()[0]
            == "succeeded"
        )
        assert store.connection.execute("SELECT COUNT(*) FROM memory_facts").fetchone()[0] == 0


def test_dream_once_is_idle_without_pending_job(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        client = FakeClient()
        result = run_dream_once(
            store,
            "worker-a",
            extractor=client,
            fact_reviewer=client,
            translator=client,
            localization_reviewer=client,
            relation_evaluator=client,
        )
        assert result.result == "idle"
        assert client.calls == 0


def test_dream_batch_stops_at_limit_and_leaves_remaining_jobs_pending(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        for index in range(3):
            store.add_source(
                f"note://batch-{index}", "The service uses SQLite for its local store."
            )
        writer = FakeClient()
        reviewer = FakeClient()

        result = run_dream_batch(
            store,
            "batch-worker",
            extractor=writer,
            fact_reviewer=reviewer,
            translator=writer,
            localization_reviewer=reviewer,
            relation_evaluator=reviewer,
            max_jobs=2,
        )

        assert result.result == "completed"
        assert result.processed_count == 2
        assert result.completed_count == 2
        assert result.error_count == 0
        assert len(result.jobs) == 2
        assert (
            store.connection.execute(
                "SELECT COUNT(*) FROM dream_jobs WHERE status = 'succeeded'"
            ).fetchone()[0]
            == 2
        )
        assert (
            store.connection.execute(
                "SELECT COUNT(*) FROM dream_jobs WHERE status = 'pending'"
            ).fetchone()[0]
            == 1
        )


def test_dream_retry_batch_leaves_pending_jobs_untouched(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source = store.add_source("note://retry", "The service uses SQLite for its local store.")
        first = store.claim_dream_job("seed-worker", now_at="2030-01-01T00:00:00Z")
        assert first is not None
        assert first.source_id == source.source_id
        store.fail_dream_job(
            first.job_id,
            "seed-worker",
            "temporary model error",
            now_at="2030-01-01T00:00:10Z",
            base_retry_seconds=20,
        )
        store.connection.execute(
            "UPDATE dream_jobs SET available_at = '2000-01-01T00:00:00Z' WHERE job_id = ?",
            (first.job_id,),
        )
        store.add_source("note://pending", "The service uses SQLite for its local store.")
        writer = FakeClient()
        reviewer = FakeClient()

        result = run_dream_batch(
            store,
            "retry-worker",
            extractor=writer,
            fact_reviewer=reviewer,
            translator=writer,
            localization_reviewer=reviewer,
            relation_evaluator=reviewer,
            max_jobs=3,
            retry_only=True,
        )

        assert result.result == "completed"
        assert result.processed_count == 1
        assert result.completed_count == 1
        assert result.error_count == 0
        assert result.jobs[0].job_id == first.job_id
        assert store.connection.execute(
            "SELECT status, COUNT(*) FROM dream_jobs GROUP BY status ORDER BY status"
        ).fetchall() == [("pending", 1), ("succeeded", 1)]


def test_dream_batch_continues_after_failed_job_and_retries_it_later(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        store.add_source("note://bad", "The service uses SQLite for its local store.")
        store.add_source("note://good", "The service uses SQLite for its local store.")
        writer = FakeClient(fail_on_uri="note://bad")
        reviewer = FakeClient()

        result = run_dream_batch(
            store,
            "batch-worker",
            extractor=writer,
            fact_reviewer=reviewer,
            translator=writer,
            localization_reviewer=reviewer,
            relation_evaluator=reviewer,
            max_jobs=10,
        )

        assert result.result == "error"
        assert result.processed_count == 2
        assert result.completed_count == 1
        assert result.error_count == 1
        assert {job.result for job in result.jobs} == {"completed", "error"}
        assert store.connection.execute(
            "SELECT status, COUNT(*) FROM dream_jobs GROUP BY status ORDER BY status"
        ).fetchall() == [("retry", 1), ("succeeded", 1)]


def test_dream_batch_requires_a_positive_job_limit(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        client = FakeClient()
        try:
            run_dream_batch(
                store,
                "batch-worker",
                extractor=client,
                fact_reviewer=client,
                translator=client,
                localization_reviewer=client,
                relation_evaluator=client,
                max_jobs=0,
            )
        except ValueError as error:
            assert "positive" in str(error)
        else:
            raise AssertionError("zero job limit should be rejected")
