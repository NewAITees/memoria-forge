import sqlite3
from pathlib import Path

import pytest

from src.memory_store import APPLICATION_ID, SCHEMA_VERSION, MemoryStore


def test_initializes_a_versioned_empty_memory_store(tmp_path: Path) -> None:
    database = tmp_path / "memory.sqlite3"

    with MemoryStore(database) as store:
        tables = {
            row[0]
            for row in store.connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        assert {
            "source_documents",
            "source_chunks",
            "entities",
            "memory_facts",
            "fact_evidence",
            "fact_entities",
            "fact_relations",
            "memory_events",
            "dream_jobs",
        } <= tables
        assert store.connection.execute("PRAGMA application_id").fetchone()[0] == APPLICATION_ID
        assert store.connection.execute("PRAGMA user_version").fetchone()[0] == SCHEMA_VERSION
        assert store.connection.execute("SELECT COUNT(*) FROM memory_facts").fetchone()[0] == 0


def test_reopening_memory_store_is_idempotent(tmp_path: Path) -> None:
    database = tmp_path / "memory.sqlite3"

    with MemoryStore(database):
        pass
    with MemoryStore(database) as store:
        assert store.connection.execute("PRAGMA user_version").fetchone()[0] == SCHEMA_VERSION
        assert store.connection.execute("SELECT COUNT(*) FROM memory_facts").fetchone()[0] == 0


def test_refuses_to_initialize_an_unrelated_existing_database(tmp_path: Path) -> None:
    database = tmp_path / "agent-state.sqlite3"
    connection = sqlite3.connect(database)
    connection.execute("CREATE TABLE existing_state (value TEXT NOT NULL)")
    connection.execute("INSERT INTO existing_state VALUES ('preserve')")
    connection.commit()
    connection.close()

    with pytest.raises(ValueError, match="not a Memoria Forge memory store"):
        MemoryStore(database)

    connection = sqlite3.connect(database)
    assert connection.execute("SELECT value FROM existing_state").fetchone() == ("preserve",)
    assert (
        connection.execute("SELECT name FROM sqlite_master WHERE name = 'memory_facts'").fetchone()
        is None
    )
    connection.close()


def test_store_enforces_relation_types_and_foreign_keys(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        store.connection.execute(
            "INSERT INTO source_documents "
            "(source_id, source_uri, content_sha256, media_type, raw_content, ingested_at) "
            "VALUES ('source-1', 'https://example.test/a', 'hash-a', 'text/html', 'raw', '2026-10-25T00:00:00Z')"
        )
        for fact_id in ("fact-1", "fact-2"):
            store.connection.execute(
                "INSERT INTO memory_facts "
                "(fact_id, statement, language, memory_type, status, confidence, recorded_at) "
                "VALUES (?, 'A verified claim', 'en', 'fact', 'active', 0.9, '2026-10-25T00:00:00Z')",
                (fact_id,),
            )
        store.connection.execute(
            "INSERT INTO fact_evidence "
            "(evidence_id, fact_id, source_id, quote, created_at) "
            "VALUES ('evidence-1', 'fact-1', 'source-1', 'A verified claim', '2026-10-25T00:00:00Z')"
        )
        store.connection.execute(
            "INSERT INTO fact_relations "
            "(relation_id, from_fact_id, to_fact_id, relation_type, confidence, status, created_at) "
            "VALUES ('edge-1', 'fact-2', 'fact-1', 'updates', 0.8, 'proposed', '2026-10-25T00:00:00Z')"
        )
        with pytest.raises(sqlite3.IntegrityError):
            store.connection.execute(
                "INSERT INTO fact_relations "
                "(relation_id, from_fact_id, to_fact_id, relation_type, confidence, status, created_at) "
                "VALUES ('edge-2', 'fact-2', 'fact-1', 'similar', 0.8, 'proposed', '2026-10-25T00:00:00Z')"
            )
        with pytest.raises(sqlite3.IntegrityError):
            store.connection.execute(
                "INSERT INTO fact_evidence "
                "(evidence_id, fact_id, source_id, quote, created_at) "
                "VALUES ('evidence-2', 'missing-fact', 'source-1', 'quote', '2026-10-25T00:00:00Z')"
            )
        store.connection.rollback()


def test_memory_events_are_append_only(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        store.connection.execute(
            "INSERT INTO memory_events (event_id, event_type, occurred_at, payload_json) "
            "VALUES ('event-1', 'source_ingested', '2026-10-25T00:00:00Z', '{}')"
        )
        with pytest.raises(sqlite3.IntegrityError, match="append-only"):
            store.connection.execute(
                "UPDATE memory_events SET payload_json = '{\"changed\": true}' WHERE event_id = 'event-1'"
            )
        store.connection.rollback()


def test_source_ingestion_is_idempotent_and_retrievable_before_dreaming(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        first = store.add_source(
            "https://example.test/hpa",
            "Kubernetes Horizontal Pod Autoscaler reads CPU metrics and adjusts replicas.",
            title="HPA metrics",
            media_type="text/html",
            max_chunk_chars=64,
        )
        duplicate = store.add_source(
            "https://example.test/hpa",
            "Kubernetes Horizontal Pod Autoscaler reads CPU metrics and adjusts replicas.",
            title="HPA metrics",
            media_type="text/html",
            max_chunk_chars=64,
        )

        assert first.created is True
        assert duplicate.created is False
        assert duplicate.source_id == first.source_id
        assert first.chunk_count > 1
        chunks = store.connection.execute(
            "SELECT content, start_offset, end_offset FROM source_chunks "
            "WHERE source_id = ? ORDER BY ordinal",
            (first.source_id,),
        ).fetchall()
        original = "Kubernetes Horizontal Pod Autoscaler reads CPU metrics and adjusts replicas."
        assert "".join(row[0] for row in chunks) == original
        assert all(original[row[1] : row[2]] == row[0] for row in chunks)

        results = store.search_sources("horizontal autoscaler", limit=5)
        assert results
        assert results[0].source_id == first.source_id
        assert store.connection.execute(
            "SELECT status FROM dream_jobs WHERE job_key = ?", (f"source:{first.source_id}",)
        ).fetchone() == ("pending",)


def test_source_revision_is_stored_as_a_new_immutable_version(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        original = store.add_source("https://example.test/guide", "The HPA target is 50 percent.")
        revised = store.add_source("https://example.test/guide", "The HPA target is 60 percent.")

        assert original.source_id != revised.source_id
        assert store.connection.execute(
            "SELECT COUNT(*) FROM source_documents WHERE source_uri = ?",
            ("https://example.test/guide",),
        ).fetchone() == (2,)


def test_fact_candidate_requires_verbatim_evidence_and_stays_pending(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source = store.add_source("note://one", "The project uses SQLite for local memory.")
        candidate = store.add_fact_candidate(
            source.source_id,
            "The project uses SQLite.",
            "The project uses SQLite for local memory.",
            language="en",
        )
        row = store.connection.execute(
            "SELECT status FROM memory_facts WHERE fact_id = ?", (candidate.fact_id,)
        ).fetchone()
        evidence = store.connection.execute(
            "SELECT start_offset, end_offset, quote FROM fact_evidence WHERE fact_id = ?",
            (candidate.fact_id,),
        ).fetchone()
        assert candidate.created is True
        assert row[0] == "pending_review"
        assert evidence[2] == "The project uses SQLite for local memory."
        assert evidence[1] - evidence[0] == len(evidence[2])
        assert (
            store.add_fact_candidate(
                source.source_id,
                "The project uses SQLite.",
                "The project uses SQLite for local memory.",
                language="en",
            ).created
            is False
        )


def test_fact_candidate_rejects_quote_not_in_source(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source = store.add_source("note://one", "The project uses SQLite.")
        with pytest.raises(ValueError, match="verbatim"):
            store.add_fact_candidate(
                source.source_id,
                "Project uses Postgres",
                "Project uses Postgres",
                language="en",
            )


def test_entity_resolution_uses_normalized_exact_aliases(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        first = store.resolve_entity("Horizontal Pod Autoscaler", "product", language="en")
        second = store.resolve_entity(" horizontal   pod autoscaler ", "product", language="en")

        assert first.created is True
        assert second.created is False
        assert second.entity_id == first.entity_id


def test_ambiguous_entity_alias_is_not_automatically_resolved(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        for entity_id, entity_type in (("mercury-place", "place"), ("mercury-org", "organization")):
            store.connection.execute(
                "INSERT INTO entities "
                "(entity_id, canonical_name, entity_type, created_at, updated_at) "
                "VALUES (?, 'Mercury', ?, 'now', 'now')",
                (entity_id, entity_type),
            )
            store.connection.execute(
                "INSERT INTO entity_aliases "
                "(entity_id, alias, language, normalized_alias, verified) "
                "VALUES (?, 'Mercury', 'en', 'mercury', 1)",
                (entity_id,),
            )

        with pytest.raises(ValueError, match="ambiguous"):
            store.resolve_entity("Mercury", "other", language="en")


def test_fact_relations_are_proposed_and_require_review(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source = store.add_source(
            "note://facts", "Old target was 50 percent. New target is 60 percent."
        )
        older = store.add_fact_candidate(
            source.source_id,
            "The old target was 50 percent.",
            "Old target was 50 percent.",
            language="en",
        )
        newer = store.add_fact_candidate(
            source.source_id,
            "The new target is 60 percent.",
            "New target is 60 percent.",
            language="en",
        )
        store.review_fact(older.fact_id, accepted=True, reviewer="reviewer")
        store.review_fact(newer.fact_id, accepted=True, reviewer="reviewer")

        relation = store.propose_fact_relation(
            newer.fact_id,
            older.fact_id,
            "updates",
            confidence=0.82,
            rationale="Both claims describe the same setting at different recorded times.",
        )
        duplicate = store.propose_fact_relation(
            newer.fact_id,
            older.fact_id,
            "updates",
            confidence=0.82,
            rationale="Both claims describe the same setting at different recorded times.",
        )
        assert relation.created is True
        assert duplicate.created is False
        assert (
            store.connection.execute(
                "SELECT status FROM fact_relations WHERE relation_id = ?", (relation.relation_id,)
            ).fetchone()[0]
            == "proposed"
        )
        store.review_fact_relation(
            relation.relation_id, accepted=True, reviewer="relation-reviewer"
        )
        assert (
            store.connection.execute(
                "SELECT status FROM fact_relations WHERE relation_id = ?", (relation.relation_id,)
            ).fetchone()[0]
            == "active"
        )


def test_relations_cannot_be_proposed_for_unreviewed_facts(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source = store.add_source("note://facts", "First claim. Second claim.")
        first = store.add_fact_candidate(
            source.source_id, "First claim.", "First claim.", language="en"
        )
        second = store.add_fact_candidate(
            source.source_id, "Second claim.", "Second claim.", language="en"
        )
        with pytest.raises(ValueError, match="active"):
            store.propose_fact_relation(first.fact_id, second.fact_id, "same", confidence=0.8)


def test_superseding_fact_preserves_history_and_recalls_by_valid_time(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source = store.add_source(
            "note://targets", "The target was 50 percent. The target is 60 percent."
        )
        old = store.add_fact_candidate(
            source.source_id,
            "The target was 50 percent.",
            "The target was 50 percent.",
            language="en",
        )
        new = store.add_fact_candidate(
            source.source_id,
            "The target is 60 percent.",
            "The target is 60 percent.",
            language="en",
        )
        store.review_fact(old.fact_id, accepted=True, reviewer="fact-reviewer")
        store.review_fact(new.fact_id, accepted=True, reviewer="fact-reviewer")

        assert store.supersede_fact(
            old.fact_id,
            new.fact_id,
            effective_at="2026-01-01T00:00:00Z",
            reviewer="update-reviewer",
            rationale="A reviewed source establishes the new target.",
        )
        assert (
            store.supersede_fact(
                old.fact_id,
                new.fact_id,
                effective_at="2026-01-01T00:00:00Z",
                reviewer="update-reviewer",
                rationale="A reviewed source establishes the new target.",
            )
            is False
        )

        old_row = store.connection.execute(
            "SELECT status, valid_to FROM memory_facts WHERE fact_id = ?", (old.fact_id,)
        ).fetchone()
        new_row = store.connection.execute(
            "SELECT status, valid_from, supersedes_fact_id FROM memory_facts WHERE fact_id = ?",
            (new.fact_id,),
        ).fetchone()
        assert old_row == ("superseded", "2026-01-01T00:00:00Z")
        assert new_row == ("active", "2026-01-01T00:00:00Z", old.fact_id)
        assert [item.fact_id for item in store.list_recall_facts("en")] == [new.fact_id]
        assert [
            item.fact_id for item in store.list_recall_facts("en", as_of="2025-06-01T00:00:00Z")
        ] == [old.fact_id]
        assert [
            item.fact_id for item in store.list_recall_facts("en", as_of="2026-06-01T00:00:00Z")
        ] == [new.fact_id]


def test_forgotten_fact_is_removed_from_current_and_historical_recall(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source = store.add_source("note://preference", "The user prefers concise reports.")
        fact = store.add_fact_candidate(
            source.source_id,
            "The user prefers concise reports.",
            "The user prefers concise reports.",
            language="en",
            memory_type="preference",
        )
        store.review_fact(fact.fact_id, accepted=True, reviewer="fact-reviewer")
        assert (
            store.forget_fact(
                fact.fact_id, reviewer="user", reason="The user asked to forget this."
            )
            is True
        )
        assert (
            store.forget_fact(
                fact.fact_id, reviewer="user", reason="The user asked to forget this."
            )
            is False
        )

        assert store.list_recall_facts("en") == []
        assert store.list_recall_facts("en", as_of="2025-01-01T00:00:00Z") == []
        assert (
            store.connection.execute(
                "SELECT event_type FROM memory_events WHERE fact_id = ? ORDER BY occurred_at DESC LIMIT 1",
                (fact.fact_id,),
            ).fetchone()[0]
            == "fact_forgotten"
        )


def test_supersede_and_recall_reject_invalid_or_unreviewed_input(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source = store.add_source("note://claims", "First claim. Second claim.")
        first = store.add_fact_candidate(
            source.source_id, "First claim.", "First claim.", language="en"
        )
        second = store.add_fact_candidate(
            source.source_id, "Second claim.", "Second claim.", language="en"
        )

        with pytest.raises(ValueError, match="active"):
            store.supersede_fact(
                first.fact_id,
                second.fact_id,
                effective_at="2026-01-01T00:00:00Z",
                reviewer="reviewer",
            )
        with pytest.raises(ValueError, match="ISO"):
            store.list_recall_facts("en", as_of="not-a-date")


def test_source_erase_removes_all_versions_derived_data_and_linked_events(tmp_path: Path) -> None:
    database = tmp_path / "memory.sqlite3"
    with MemoryStore(database) as store:
        first = store.add_source("note://private", "Private fact: the target is 50 percent.")
        revised = store.add_source("note://private", "Private fact: the target is 60 percent.")
        old = store.add_fact_candidate(
            first.source_id,
            "The target is 50 percent.",
            "Private fact: the target is 50 percent.",
            language="en",
        )
        derived = store.add_fact_candidate(
            revised.source_id,
            "The target is probably unstable.",
            "Private fact: the target is 60 percent.",
            language="en",
            memory_type="inference",
        )
        store.review_fact(old.fact_id, accepted=True, reviewer="reviewer")
        store.review_fact(derived.fact_id, accepted=True, reviewer="reviewer")
        store.propose_fact_relation(
            derived.fact_id,
            old.fact_id,
            "derived_from",
            confidence=0.8,
            rationale="Derived from source measurements.",
        )
        store.resolve_entity("Private target", "concept")
        store.connection.execute(
            "INSERT INTO fact_entities (fact_id, entity_id, role) "
            "SELECT ?, entity_id, 'mentioned' FROM entities WHERE canonical_name = 'Private target'",
            (old.fact_id,),
        )

        result = store.erase_source(first.source_id)

        assert result.source_count == 2
        assert result.fact_count == 2
        assert result.relation_count == 1
        assert store.connection.execute("SELECT COUNT(*) FROM source_documents").fetchone()[0] == 0
        assert store.connection.execute("SELECT COUNT(*) FROM source_chunks").fetchone()[0] == 0
        assert store.connection.execute("SELECT COUNT(*) FROM memory_facts").fetchone()[0] == 0
        assert store.connection.execute("SELECT COUNT(*) FROM fact_relations").fetchone()[0] == 0
        assert store.connection.execute("SELECT COUNT(*) FROM fact_entities").fetchone()[0] == 0
        events = store.connection.execute(
            "SELECT event_type, fact_id, source_id, payload_json FROM memory_events"
        ).fetchall()
        assert events == [("source_deleted", None, None, '{"erased":true}')]
        assert store.connection.execute("SELECT COUNT(*) FROM dream_jobs").fetchone()[0] == 0


def test_recalls_only_current_approved_facts_from_matching_sources(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source = store.add_source(
            "https://example.test/hpa",
            "Horizontal Pod Autoscaler (HPA) scales from 2 to 6 replicas.",
            title="HPA docs",
        )
        fact = store.add_fact_candidate(
            source.source_id,
            "The HPA scales from 2 to 6 replicas.",
            "Horizontal Pod Autoscaler (HPA) scales from 2 to 6 replicas.",
            language="en",
        )
        store.review_fact(fact.fact_id, accepted=True, reviewer="fact-reviewer")
        store.save_localization(fact.fact_id, "ja", "HPAは2から6レプリカへ拡張する。")
        store.review_localization(
            fact.fact_id, "ja", approved=True, reviewer="translation-reviewer"
        )

        recalled = store.search_recall_facts("horizontal autoscaler", "ja")

        assert len(recalled) == 1
        assert recalled[0].fact_id == fact.fact_id
        assert recalled[0].statement == "HPAは2から6レプリカへ拡張する。"
        assert recalled[0].source_uri == "https://example.test/hpa"
        assert (
            recalled[0].evidence_quote
            == "Horizontal Pod Autoscaler (HPA) scales from 2 to 6 replicas."
        )
        store.forget_fact(fact.fact_id, reviewer="user", reason="Forget this fact.")
        assert store.search_recall_facts("horizontal autoscaler", "ja") == []


def test_memory_store_v1_migrates_event_delete_guard_to_v2(tmp_path: Path) -> None:
    database = tmp_path / "memory.sqlite3"
    with MemoryStore(database) as store:
        store.connection.execute("DROP TRIGGER memory_events_no_delete")
        store.connection.execute(
            "CREATE TRIGGER memory_events_no_delete BEFORE DELETE ON memory_events "
            "BEGIN SELECT RAISE(ABORT, 'memory_events is append-only'); END"
        )
        store.connection.execute("DELETE FROM schema_migrations WHERE version = 2")
        store.connection.execute("PRAGMA user_version = 1")
        store.connection.commit()

    with MemoryStore(database) as migrated:
        assert migrated.connection.execute("PRAGMA user_version").fetchone()[0] == 2
        migrated.connection.execute(
            "INSERT INTO memory_events (event_id, event_type, occurred_at, payload_json) "
            "VALUES ('keep', 'source_ingested', '2026-01-01T00:00:00Z', '{}')"
        )
        with pytest.raises(sqlite3.IntegrityError, match="append-only"):
            migrated.connection.execute("DELETE FROM memory_events WHERE event_id = 'keep'")


def test_dream_job_claim_retry_and_completion_are_leased_and_idempotent(tmp_path: Path) -> None:
    database = tmp_path / "memory.sqlite3"
    with MemoryStore(database) as first_worker, MemoryStore(database) as second_worker:
        source = first_worker.add_source("note://dream", "A source for Dreaming.")
        first = first_worker.claim_dream_job(
            "worker-a", lease_seconds=60, now_at="2030-01-01T00:00:00Z"
        )
        assert first is not None
        assert first.source_id == source.source_id
        assert first.attempts == 1
        assert (
            second_worker.claim_dream_job(
                "worker-b", lease_seconds=60, now_at="2030-01-01T00:00:30Z"
            )
            is None
        )

        failed = first_worker.fail_dream_job(
            first.job_id,
            "worker-a",
            "temporary model error",
            now_at="2030-01-01T00:00:10Z",
            base_retry_seconds=20,
            max_attempts=3,
        )
        assert failed.status == "retry"
        assert failed.available_at == "2030-01-01T00:00:30Z"
        assert (
            second_worker.claim_dream_job(
                "worker-b", lease_seconds=60, now_at="2030-01-01T00:00:29Z"
            )
            is None
        )
        retry = second_worker.claim_dream_job(
            "worker-b", lease_seconds=60, now_at="2030-01-01T00:00:30Z"
        )
        assert retry is not None
        assert retry.job_id == first.job_id
        assert retry.attempts == 2
        assert second_worker.complete_dream_job(retry.job_id, "worker-b") is True
        assert second_worker.complete_dream_job(retry.job_id, "worker-b") is False
        assert first_worker.connection.execute(
            "SELECT status, attempts FROM dream_jobs WHERE job_id = ?", (first.job_id,)
        ).fetchone() == ("succeeded", 2)


def test_retry_only_claim_does_not_claim_pending_jobs(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        retry_source = store.add_source("note://retry", "A source for retry.")
        first = store.claim_dream_job("worker-a", now_at="2030-01-01T00:00:00Z")
        assert first is not None
        assert first.source_id == retry_source.source_id
        store.fail_dream_job(
            first.job_id,
            "worker-a",
            "temporary model error",
            now_at="2030-01-01T00:00:10Z",
            base_retry_seconds=20,
        )
        pending_source = store.add_source("note://pending", "A source that stays pending.")

        retry = store.claim_dream_job("worker-b", retry_only=True, now_at="2030-01-01T00:00:30Z")

        assert retry is not None
        assert retry.job_id == first.job_id
        assert retry.attempts == 2
        pending_job = store.connection.execute(
            "SELECT status FROM dream_jobs WHERE payload_json LIKE ?",
            (f"%{pending_source.source_id}%",),
        ).fetchone()
        assert pending_job == ("pending",)


def test_expired_dream_lease_can_be_reclaimed_by_another_worker(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        store.add_source("note://dream", "A source for Dreaming.")
        first = store.claim_dream_job("worker-a", lease_seconds=10, now_at="2030-01-01T00:00:00Z")
        assert first is not None
        reclaimed = store.claim_dream_job(
            "worker-b", lease_seconds=10, now_at="2030-01-01T00:00:11Z"
        )
        assert reclaimed is not None
        assert reclaimed.job_id == first.job_id
        assert reclaimed.attempts == 2
        assert reclaimed.lease_owner == "worker-b"


def test_dream_job_final_failure_stops_after_max_attempts(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        store.add_source("note://dream", "A source for Dreaming.")
        first = store.claim_dream_job("worker-a", lease_seconds=10, now_at="2030-01-01T00:00:00Z")
        assert first is not None
        result = store.fail_dream_job(
            first.job_id,
            "worker-a",
            "permanent model error",
            now_at="2030-01-01T00:00:01Z",
            max_attempts=1,
        )
        assert result.status == "failed"
        assert (
            store.claim_dream_job("worker-b", lease_seconds=10, now_at="2030-01-02T00:00:00Z")
            is None
        )


def test_only_reviewed_facts_can_be_activated_and_review_is_recorded(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source = store.add_source("note://one", "The project uses SQLite for local memory.")
        candidate = store.add_fact_candidate(
            source.source_id,
            "The project uses SQLite.",
            "The project uses SQLite for local memory.",
            language="en",
        )
        store.review_fact(candidate.fact_id, accepted=True, reviewer="reviewer-v1")

        status = store.connection.execute(
            "SELECT status FROM memory_facts WHERE fact_id = ?", (candidate.fact_id,)
        ).fetchone()[0]
        event = store.connection.execute(
            "SELECT event_type, payload_json FROM memory_events WHERE fact_id = ? "
            "AND event_type = 'fact_reviewed'",
            (candidate.fact_id,),
        ).fetchone()
        assert status == "active"
        assert event[0] == "fact_reviewed"
        assert '"accepted": true' in event[1]


def test_localization_requires_active_fact_and_explicit_review(tmp_path: Path) -> None:
    with MemoryStore(tmp_path / "memory.sqlite3") as store:
        source = store.add_source("note://one", "The project uses SQLite for local memory.")
        candidate = store.add_fact_candidate(
            source.source_id,
            "The project uses SQLite.",
            "The project uses SQLite for local memory.",
            language="en",
        )
        with pytest.raises(ValueError, match="active"):
            store.save_localization(candidate.fact_id, "ja", "このプロジェクトはSQLiteを使う")

        store.review_fact(candidate.fact_id, accepted=True, reviewer="reviewer-v1")
        store.save_localization(candidate.fact_id, "ja", "このプロジェクトはSQLiteを使う")
        with pytest.raises(ValueError, match="approved"):
            store.get_recall_statement(candidate.fact_id, "ja")
        store.review_localization(
            candidate.fact_id, "ja", approved=True, reviewer="translator-review-v1"
        )
        assert (
            store.get_recall_statement(candidate.fact_id, "ja") == "このプロジェクトはSQLiteを使う"
        )
