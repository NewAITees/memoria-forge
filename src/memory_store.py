"""Versioned empty-store schema for the local memory engine.

Design: docs/local_memory_engine_plan_2026-10-25.md
Related: src.wiki_agent.StateDB (existing app state), src.atomic_facts (prior prototype)
"""

from __future__ import annotations

import sqlite3
import hashlib
import json
import re
import unicodedata
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


APPLICATION_ID = 0x4D464D45  # ASCII "MFME"
SCHEMA_VERSION = 3

_REQUIRED_TABLES = frozenset(
    {
        "schema_migrations",
        "source_documents",
        "source_chunks",
        "source_chunk_search",
        "entities",
        "entity_aliases",
        "entity_alias_reviews",
        "memory_facts",
        "memory_localizations",
        "fact_evidence",
        "fact_entities",
        "fact_relations",
        "memory_events",
        "dream_jobs",
    }
)

_SCHEMA = """
CREATE TABLE schema_migrations (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);

CREATE TABLE source_documents (
    source_id TEXT PRIMARY KEY,
    source_uri TEXT NOT NULL,
    title TEXT NOT NULL DEFAULT '',
    media_type TEXT NOT NULL,
    content_sha256 TEXT NOT NULL,
    raw_content TEXT NOT NULL,
    document_at TEXT,
    ingested_at TEXT NOT NULL,
    source_state TEXT NOT NULL DEFAULT 'active'
        CHECK (source_state IN ('active', 'revoked', 'deleted')),
    UNIQUE (source_uri, content_sha256)
);

CREATE INDEX source_documents_uri_idx ON source_documents(source_uri);
CREATE INDEX source_documents_ingested_idx ON source_documents(ingested_at);

CREATE TABLE source_chunks (
    chunk_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL REFERENCES source_documents(source_id) ON DELETE CASCADE,
    ordinal INTEGER NOT NULL CHECK (ordinal >= 0),
    content TEXT NOT NULL,
    start_offset INTEGER NOT NULL CHECK (start_offset >= 0),
    end_offset INTEGER NOT NULL CHECK (end_offset >= start_offset),
    UNIQUE (source_id, ordinal)
);

CREATE TABLE entities (
    entity_id TEXT PRIMARY KEY,
    canonical_name TEXT NOT NULL,
    entity_type TEXT NOT NULL
        CHECK (entity_type IN ('person', 'organization', 'product', 'project', 'place', 'event', 'concept', 'other')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE VIRTUAL TABLE source_chunk_search USING fts5(
    chunk_id UNINDEXED,
    source_id UNINDEXED,
    ordinal UNINDEXED,
    content,
    tokenize = 'unicode61 remove_diacritics 2'
);

CREATE TRIGGER source_chunks_search_insert
AFTER INSERT ON source_chunks
BEGIN
    INSERT INTO source_chunk_search (chunk_id, source_id, ordinal, content)
    VALUES (new.chunk_id, new.source_id, new.ordinal, new.content);
END;

CREATE TRIGGER source_chunks_search_delete
AFTER DELETE ON source_chunks
BEGIN
    DELETE FROM source_chunk_search WHERE chunk_id = old.chunk_id;
END;

CREATE TRIGGER source_chunks_search_update
AFTER UPDATE ON source_chunks
BEGIN
    DELETE FROM source_chunk_search WHERE chunk_id = old.chunk_id;
    INSERT INTO source_chunk_search (chunk_id, source_id, ordinal, content)
    VALUES (new.chunk_id, new.source_id, new.ordinal, new.content);
END;

CREATE TABLE entity_aliases (
    entity_id TEXT NOT NULL REFERENCES entities(entity_id) ON DELETE CASCADE,
    alias TEXT NOT NULL,
    language TEXT NOT NULL DEFAULT '',
    normalized_alias TEXT NOT NULL,
    verified INTEGER NOT NULL DEFAULT 0 CHECK (verified IN (0, 1)),
    PRIMARY KEY (entity_id, normalized_alias)
);

CREATE INDEX entity_aliases_lookup_idx ON entity_aliases(normalized_alias);

CREATE TABLE entity_alias_reviews (
    review_id TEXT PRIMARY KEY,
    entity_id TEXT NOT NULL,
    normalized_alias TEXT NOT NULL,
    reviewer TEXT NOT NULL,
    reason TEXT NOT NULL,
    reviewed_at TEXT NOT NULL,
    FOREIGN KEY (entity_id, normalized_alias)
        REFERENCES entity_aliases(entity_id, normalized_alias) ON DELETE CASCADE
);

CREATE INDEX entity_alias_reviews_entity_idx
    ON entity_alias_reviews(entity_id, normalized_alias, reviewed_at);

CREATE TRIGGER entity_alias_reviews_no_update
BEFORE UPDATE ON entity_alias_reviews
BEGIN
    SELECT RAISE(ABORT, 'entity_alias_reviews is append-only');
END;

CREATE TRIGGER entity_alias_reviews_no_delete
BEFORE DELETE ON entity_alias_reviews
WHEN memory_erase_authorized() = 0
BEGIN
    SELECT RAISE(ABORT, 'entity_alias_reviews is append-only');
END;

CREATE TABLE memory_facts (
    fact_id TEXT PRIMARY KEY,
    statement TEXT NOT NULL,
    language TEXT NOT NULL,
    memory_type TEXT NOT NULL
        CHECK (memory_type IN ('fact', 'preference', 'episode', 'inference')),
    status TEXT NOT NULL
        CHECK (status IN ('pending_review', 'active', 'superseded', 'forgotten', 'expired', 'rejected')),
    confidence REAL NOT NULL CHECK (confidence >= 0.0 AND confidence <= 1.0),
    valid_from TEXT,
    valid_to TEXT,
    recorded_at TEXT NOT NULL,
    supersedes_fact_id TEXT REFERENCES memory_facts(fact_id) ON DELETE RESTRICT,
    CHECK (valid_to IS NULL OR valid_from IS NULL OR valid_to >= valid_from)
);

CREATE INDEX memory_facts_current_idx ON memory_facts(status, memory_type);
CREATE INDEX memory_facts_validity_idx ON memory_facts(valid_from, valid_to);

CREATE TABLE memory_localizations (
    fact_id TEXT NOT NULL REFERENCES memory_facts(fact_id) ON DELETE CASCADE,
    locale TEXT NOT NULL,
    statement TEXT NOT NULL,
    review_status TEXT NOT NULL
        CHECK (review_status IN ('pending', 'approved', 'rejected')),
    reviewer_note TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    PRIMARY KEY (fact_id, locale)
);

CREATE TABLE fact_evidence (
    evidence_id TEXT PRIMARY KEY,
    fact_id TEXT NOT NULL REFERENCES memory_facts(fact_id) ON DELETE CASCADE,
    source_id TEXT NOT NULL REFERENCES source_documents(source_id) ON DELETE RESTRICT,
    quote TEXT NOT NULL,
    start_offset INTEGER,
    end_offset INTEGER,
    evidence_role TEXT NOT NULL DEFAULT 'supports'
        CHECK (evidence_role IN ('supports', 'contradicts')),
    created_at TEXT NOT NULL,
    CHECK (start_offset IS NULL OR start_offset >= 0),
    CHECK (end_offset IS NULL OR start_offset IS NULL OR end_offset >= start_offset)
);

CREATE INDEX fact_evidence_fact_idx ON fact_evidence(fact_id);
CREATE INDEX fact_evidence_source_idx ON fact_evidence(source_id);

CREATE TABLE fact_entities (
    fact_id TEXT NOT NULL REFERENCES memory_facts(fact_id) ON DELETE CASCADE,
    entity_id TEXT NOT NULL REFERENCES entities(entity_id) ON DELETE RESTRICT,
    role TEXT NOT NULL CHECK (role IN ('subject', 'object', 'mentioned')),
    PRIMARY KEY (fact_id, entity_id, role)
);

CREATE TABLE fact_relations (
    relation_id TEXT PRIMARY KEY,
    from_fact_id TEXT NOT NULL REFERENCES memory_facts(fact_id) ON DELETE CASCADE,
    to_fact_id TEXT NOT NULL REFERENCES memory_facts(fact_id) ON DELETE CASCADE,
    relation_type TEXT NOT NULL
        CHECK (relation_type IN ('same', 'extends', 'updates', 'contradicts', 'derived_from')),
    confidence REAL NOT NULL CHECK (confidence >= 0.0 AND confidence <= 1.0),
    status TEXT NOT NULL CHECK (status IN ('proposed', 'active', 'rejected', 'superseded')),
    rationale TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    reviewed_at TEXT,
    CHECK (from_fact_id <> to_fact_id),
    UNIQUE (from_fact_id, to_fact_id, relation_type)
);

CREATE INDEX fact_relations_from_idx ON fact_relations(from_fact_id, status);
CREATE INDEX fact_relations_to_idx ON fact_relations(to_fact_id, status);

CREATE TABLE memory_events (
    event_id TEXT PRIMARY KEY,
    fact_id TEXT,
    source_id TEXT,
    event_type TEXT NOT NULL
        CHECK (event_type IN (
            'source_ingested', 'source_revoked', 'source_deleted',
            'fact_asserted', 'fact_reviewed', 'fact_superseded', 'fact_forgotten',
            'fact_expired', 'fact_restored', 'relation_proposed', 'relation_reviewed',
            'dream_started', 'dream_completed', 'dream_failed'
        )),
    occurred_at TEXT NOT NULL,
    payload_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(payload_json)),
    idempotency_key TEXT UNIQUE
);

CREATE INDEX memory_events_fact_idx ON memory_events(fact_id, occurred_at);
CREATE INDEX memory_events_source_idx ON memory_events(source_id, occurred_at);

CREATE TRIGGER memory_events_no_update
BEFORE UPDATE ON memory_events
BEGIN
    SELECT RAISE(ABORT, 'memory_events is append-only');
END;

CREATE TRIGGER memory_events_no_delete
BEFORE DELETE ON memory_events
WHEN memory_erase_authorized() = 0
BEGIN
    SELECT RAISE(ABORT, 'memory_events is append-only');
END;

CREATE TABLE dream_jobs (
    job_id TEXT PRIMARY KEY,
    job_key TEXT NOT NULL UNIQUE,
    trigger_type TEXT NOT NULL
        CHECK (trigger_type IN ('new_source', 'batch_threshold', 'quiet_period', 'manual', 'retry')),
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'running', 'retry', 'succeeded', 'failed')),
    payload_json TEXT NOT NULL DEFAULT '{}' CHECK (json_valid(payload_json)),
    attempts INTEGER NOT NULL DEFAULT 0 CHECK (attempts >= 0),
    available_at TEXT NOT NULL,
    lease_owner TEXT,
    lease_expires_at TEXT,
    last_error TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    completed_at TEXT
);

CREATE INDEX dream_jobs_ready_idx ON dream_jobs(status, available_at);
"""


@dataclass(frozen=True)
class SourceWriteResult:
    source_id: str
    content_sha256: str
    chunk_count: int
    created: bool


@dataclass(frozen=True)
class SourceSearchResult:
    source_id: str
    source_uri: str
    title: str
    chunk_id: str
    ordinal: int
    content: str
    score: float


@dataclass(frozen=True)
class SourceListEntry:
    source_id: str
    source_uri: str
    title: str
    media_type: str
    source_state: str
    ingested_at: str
    chunk_count: int


@dataclass(frozen=True)
class FactWriteResult:
    fact_id: str
    evidence_id: str
    status: str
    created: bool


@dataclass(frozen=True)
class EntityWriteResult:
    entity_id: str
    canonical_name: str
    entity_type: str
    created: bool


@dataclass(frozen=True)
class EntityAliasWriteResult:
    entity_id: str
    alias: str
    normalized_alias: str
    created: bool


@dataclass(frozen=True)
class RelationWriteResult:
    relation_id: str
    status: str
    created: bool


@dataclass(frozen=True)
class RecallFact:
    fact_id: str
    statement: str
    language: str
    memory_type: str
    confidence: float
    valid_from: str | None
    valid_to: str | None
    source_uri: str | None = None
    source_title: str | None = None
    evidence_quote: str | None = None


@dataclass(frozen=True)
class SourceEraseResult:
    source_count: int
    fact_count: int
    relation_count: int
    dream_job_count: int


@dataclass(frozen=True)
class DreamJob:
    job_id: str
    job_key: str
    trigger_type: str
    payload: dict[str, object]
    attempts: int
    lease_owner: str
    lease_expires_at: str

    @property
    def source_id(self) -> str | None:
        value = self.payload.get("source_id")
        return value if isinstance(value, str) else None


@dataclass(frozen=True)
class DreamJobResult:
    job_id: str
    status: str
    attempts: int
    available_at: str


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _normalize_entity_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    return " ".join(re.findall(r"[\w]+", normalized, flags=re.UNICODE))


def _normalize_timestamp(value: str) -> str:
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError("timestamp must be ISO 8601 with a timezone") from error
    if parsed.tzinfo is None:
        raise ValueError("timestamp must include a timezone")
    return parsed.astimezone(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def _split_source_content(content: str, max_chunk_chars: int) -> list[tuple[int, int, str]]:
    if max_chunk_chars < 1:
        raise ValueError("max_chunk_chars must be positive")
    chunks: list[tuple[int, int, str]] = []
    start = 0
    while start < len(content):
        end = min(start + max_chunk_chars, len(content))
        if end < len(content):
            floor = start + max_chunk_chars // 2
            boundaries = [content.rfind(separator, floor, end) for separator in ("\n\n", "\n", " ")]
            boundary = max(boundaries)
            if boundary > start:
                end = boundary + (2 if content.startswith("\n\n", boundary) else 1)
        chunks.append((start, end, content[start:end]))
        start = end
    return chunks


class MemoryStore:
    """Own the new local memory database without migrating legacy agent state."""

    def __init__(self, path: Path) -> None:
        self.path = path.resolve()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(self.path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self._erase_authorized = False
        self.connection.create_function(
            "memory_erase_authorized", 0, lambda: int(self._erase_authorized)
        )
        try:
            self._initialize_or_validate()
        except Exception:
            self.connection.close()
            raise

    def _initialize_or_validate(self) -> None:
        application_id = int(self.connection.execute("PRAGMA application_id").fetchone()[0])
        version = int(self.connection.execute("PRAGMA user_version").fetchone()[0])
        tables = {
            str(row[0])
            for row in self.connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
            )
        }

        if application_id == 0 and version == 0 and not tables:
            self._create_schema()
            return
        if application_id != APPLICATION_ID:
            raise ValueError(f"{self.path} is not a Memoria Forge memory store")
        if version == 1:
            missing = (_REQUIRED_TABLES - {"entity_alias_reviews"}) - tables
            if missing:
                raise ValueError("memory store schema is incomplete: " + ", ".join(sorted(missing)))
            self._migrate_v1_to_v2()
            version = 2
        if version == 2:
            self._migrate_v2_to_v3()
            version = 3
            tables.add("entity_alias_reviews")
        if version != SCHEMA_VERSION:
            raise ValueError(
                f"unsupported memory store schema version {version}; expected {SCHEMA_VERSION}"
            )
        missing = _REQUIRED_TABLES - tables
        if missing:
            raise ValueError("memory store schema is incomplete: " + ", ".join(sorted(missing)))

    def _migrate_v1_to_v2(self) -> None:
        with self.connection:
            self.connection.execute("DROP TRIGGER IF EXISTS memory_events_no_delete")
            self.connection.execute(
                "CREATE TRIGGER memory_events_no_delete BEFORE DELETE ON memory_events "
                "WHEN memory_erase_authorized() = 0 "
                "BEGIN SELECT RAISE(ABORT, 'memory_events is append-only'); END"
            )
            self.connection.execute(
                "INSERT INTO schema_migrations (version, applied_at) "
                "VALUES (2, strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))"
            )
            self.connection.execute("PRAGMA user_version = 2")

    def _migrate_v2_to_v3(self) -> None:
        script = """
        BEGIN IMMEDIATE;
        CREATE TABLE entity_alias_reviews (
            review_id TEXT PRIMARY KEY,
            entity_id TEXT NOT NULL,
            normalized_alias TEXT NOT NULL,
            reviewer TEXT NOT NULL,
            reason TEXT NOT NULL,
            reviewed_at TEXT NOT NULL,
            FOREIGN KEY (entity_id, normalized_alias)
                REFERENCES entity_aliases(entity_id, normalized_alias) ON DELETE CASCADE
        );
        CREATE INDEX entity_alias_reviews_entity_idx
            ON entity_alias_reviews(entity_id, normalized_alias, reviewed_at);
        CREATE TRIGGER entity_alias_reviews_no_update
        BEFORE UPDATE ON entity_alias_reviews
        BEGIN
            SELECT RAISE(ABORT, 'entity_alias_reviews is append-only');
        END;
        CREATE TRIGGER entity_alias_reviews_no_delete
        BEFORE DELETE ON entity_alias_reviews
        WHEN memory_erase_authorized() = 0
        BEGIN
            SELECT RAISE(ABORT, 'entity_alias_reviews is append-only');
        END;
        INSERT INTO schema_migrations (version, applied_at)
            VALUES (3, strftime('%Y-%m-%dT%H:%M:%fZ', 'now'));
        PRAGMA user_version = 3;
        COMMIT;
        """
        try:
            self.connection.executescript(script)
        except sqlite3.Error:
            if self.connection.in_transaction:
                self.connection.rollback()
            raise

    def _create_schema(self) -> None:
        script = (
            "BEGIN IMMEDIATE;\n"
            + _SCHEMA
            + f"\nINSERT INTO schema_migrations (version, applied_at) "
            f"VALUES ({SCHEMA_VERSION}, strftime('%Y-%m-%dT%H:%M:%fZ', 'now'));\n"
            + f"PRAGMA application_id = {APPLICATION_ID};\n"
            + f"PRAGMA user_version = {SCHEMA_VERSION};\n"
            + "COMMIT;"
        )
        try:
            self.connection.executescript(script)
        except sqlite3.Error:
            if self.connection.in_transaction:
                self.connection.rollback()
            raise

    def add_source(
        self,
        source_uri: str,
        raw_content: str,
        *,
        title: str = "",
        media_type: str = "text/plain",
        document_at: str | None = None,
        max_chunk_chars: int = 3000,
    ) -> SourceWriteResult:
        uri = source_uri.strip()
        if not uri:
            raise ValueError("source_uri must not be empty")
        if not raw_content:
            raise ValueError("raw_content must not be empty")
        if not media_type.strip():
            raise ValueError("media_type must not be empty")
        chunks = _split_source_content(raw_content, max_chunk_chars)
        content_hash = hashlib.sha256(raw_content.encode("utf-8")).hexdigest()
        existing = self.connection.execute(
            "SELECT source_id FROM source_documents WHERE source_uri = ? AND content_sha256 = ?",
            (uri, content_hash),
        ).fetchone()
        if existing:
            chunk_count = self.connection.execute(
                "SELECT COUNT(*) FROM source_chunks WHERE source_id = ?", (existing[0],)
            ).fetchone()[0]
            return SourceWriteResult(str(existing[0]), content_hash, int(chunk_count), False)

        source_id = hashlib.sha256(f"{uri}\0{content_hash}".encode("utf-8")).hexdigest()[:32]
        now = _utc_now()
        with self.connection:
            self.connection.execute(
                "INSERT INTO source_documents "
                "(source_id, source_uri, title, media_type, content_sha256, raw_content, "
                "document_at, ingested_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    source_id,
                    uri,
                    title.strip(),
                    media_type.strip(),
                    content_hash,
                    raw_content,
                    document_at,
                    now,
                ),
            )
            for ordinal, (start, end, text) in enumerate(chunks):
                chunk_id = hashlib.sha256(
                    f"{source_id}:{ordinal}:{start}:{end}".encode("utf-8")
                ).hexdigest()[:32]
                self.connection.execute(
                    "INSERT INTO source_chunks "
                    "(chunk_id, source_id, ordinal, content, start_offset, end_offset) "
                    "VALUES (?, ?, ?, ?, ?, ?)",
                    (chunk_id, source_id, ordinal, text, start, end),
                )
            self.connection.execute(
                "INSERT INTO memory_events "
                "(event_id, source_id, event_type, occurred_at, payload_json, idempotency_key) "
                "VALUES (?, ?, 'source_ingested', ?, ?, ?)",
                (
                    hashlib.sha256(f"event:source:{source_id}".encode()).hexdigest()[:32],
                    source_id,
                    now,
                    json.dumps({"source_id": source_id, "content_sha256": content_hash}),
                    f"source-ingested:{source_id}",
                ),
            )
            self.connection.execute(
                "INSERT INTO dream_jobs "
                "(job_id, job_key, trigger_type, status, payload_json, available_at, created_at, updated_at) "
                "VALUES (?, ?, 'new_source', 'pending', ?, ?, ?, ?)",
                (
                    hashlib.sha256(f"dream:{source_id}".encode()).hexdigest()[:32],
                    f"source:{source_id}",
                    json.dumps({"source_id": source_id}),
                    now,
                    now,
                    now,
                ),
            )
        return SourceWriteResult(source_id, content_hash, len(chunks), True)

    def claim_dream_job(
        self,
        worker_id: str,
        *,
        lease_seconds: int = 300,
        now_at: str | None = None,
        retry_only: bool = False,
    ) -> DreamJob | None:
        worker = worker_id.strip()
        if not worker or lease_seconds < 1:
            raise ValueError("worker_id and positive lease_seconds are required")
        now = _normalize_timestamp(now_at or _utc_now())
        now_dt = datetime.fromisoformat(now.replace("Z", "+00:00"))
        expires = now_dt.timestamp() + lease_seconds
        lease_until = (
            datetime.fromtimestamp(expires, timezone.utc)
            .isoformat(timespec="seconds")
            .replace("+00:00", "Z")
        )
        with self.connection:
            self.connection.execute("BEGIN IMMEDIATE")
            if retry_only:
                row = self.connection.execute(
                    "SELECT job_id, job_key, trigger_type, payload_json, attempts FROM dream_jobs "
                    "WHERE status = 'retry' AND available_at <= ? "
                    "ORDER BY available_at, created_at, job_id LIMIT 1",
                    (now,),
                ).fetchone()
            else:
                row = self.connection.execute(
                    "SELECT job_id, job_key, trigger_type, payload_json, attempts FROM dream_jobs "
                    "WHERE ((status IN ('pending', 'retry') AND available_at <= ?) "
                    "OR (status = 'running' AND (lease_expires_at IS NULL OR lease_expires_at <= ?))) "
                    "ORDER BY available_at, created_at, job_id LIMIT 1",
                    (now, now),
                ).fetchone()
            if row is None:
                return None
            job_id, job_key, trigger_type, payload_json, attempts = row
            attempt = int(attempts) + 1
            self.connection.execute(
                "UPDATE dream_jobs SET status = 'running', attempts = ?, lease_owner = ?, "
                "lease_expires_at = ?, updated_at = ?, last_error = '' WHERE job_id = ?",
                (attempt, worker, lease_until, now, job_id),
            )
            payload = json.loads(str(payload_json))
            source_id = payload.get("source_id") if isinstance(payload, dict) else None
            self.connection.execute(
                "INSERT INTO memory_events (event_id, source_id, event_type, occurred_at, "
                "payload_json, idempotency_key) VALUES (?, ?, 'dream_started', ?, ?, ?)",
                (
                    uuid.uuid4().hex,
                    source_id,
                    now,
                    json.dumps({"job_id": job_id, "attempt": attempt, "worker": worker}),
                    f"dream-started:{job_id}:{attempt}",
                ),
            )
        return DreamJob(
            str(job_id), str(job_key), str(trigger_type), payload, attempt, worker, lease_until
        )

    def complete_dream_job(self, job_id: str, worker_id: str, *, now_at: str | None = None) -> bool:
        now = _normalize_timestamp(now_at or _utc_now())
        with self.connection:
            row = self.connection.execute(
                "SELECT status, lease_owner, attempts, payload_json FROM dream_jobs WHERE job_id = ?",
                (job_id,),
            ).fetchone()
            if row is None:
                raise ValueError("dream job does not exist")
            if row[0] == "succeeded":
                return False
            if row[0] != "running" or row[1] != worker_id:
                raise ValueError("dream job is not leased by this worker")
            self.connection.execute(
                "UPDATE dream_jobs SET status = 'succeeded', lease_owner = NULL, "
                "lease_expires_at = NULL, updated_at = ?, completed_at = ? WHERE job_id = ?",
                (now, now, job_id),
            )
            payload = json.loads(str(row[3]))
            source_id = payload.get("source_id") if isinstance(payload, dict) else None
            self.connection.execute(
                "INSERT INTO memory_events (event_id, source_id, event_type, occurred_at, "
                "payload_json, idempotency_key) VALUES (?, ?, 'dream_completed', ?, ?, ?)",
                (
                    uuid.uuid4().hex,
                    source_id,
                    now,
                    json.dumps({"job_id": job_id, "attempt": row[2]}),
                    f"dream-completed:{job_id}",
                ),
            )
        return True

    def fail_dream_job(
        self,
        job_id: str,
        worker_id: str,
        error: str,
        *,
        now_at: str | None = None,
        base_retry_seconds: int = 30,
        max_attempts: int = 5,
        max_retry_seconds: int = 3600,
    ) -> DreamJobResult:
        if base_retry_seconds < 1 or max_attempts < 1 or max_retry_seconds < 1:
            raise ValueError("retry limits must be positive")
        message = error.strip()
        if not message:
            raise ValueError("error must not be empty")
        now = _normalize_timestamp(now_at or _utc_now())
        with self.connection:
            row = self.connection.execute(
                "SELECT status, lease_owner, attempts, payload_json FROM dream_jobs WHERE job_id = ?",
                (job_id,),
            ).fetchone()
            if row is None:
                raise ValueError("dream job does not exist")
            if row[0] != "running" or row[1] != worker_id:
                raise ValueError("dream job is not leased by this worker")
            attempts = int(row[2])
            status = "failed" if attempts >= max_attempts else "retry"
            delay = min(base_retry_seconds * (2 ** (attempts - 1)), max_retry_seconds)
            now_dt = datetime.fromisoformat(now.replace("Z", "+00:00"))
            available_at = (
                datetime.fromtimestamp(
                    now_dt.timestamp() + (delay if status == "retry" else 0), timezone.utc
                )
                .isoformat(timespec="seconds")
                .replace("+00:00", "Z")
            )
            self.connection.execute(
                "UPDATE dream_jobs SET status = ?, available_at = ?, lease_owner = NULL, "
                "lease_expires_at = NULL, last_error = ?, updated_at = ? WHERE job_id = ?",
                (status, available_at, message[:2000], now, job_id),
            )
            payload = json.loads(str(row[3]))
            source_id = payload.get("source_id") if isinstance(payload, dict) else None
            self.connection.execute(
                "INSERT INTO memory_events (event_id, source_id, event_type, occurred_at, "
                "payload_json, idempotency_key) VALUES (?, ?, 'dream_failed', ?, ?, ?)",
                (
                    uuid.uuid4().hex,
                    source_id,
                    now,
                    json.dumps({"job_id": job_id, "attempt": attempts, "error": message[:2000]}),
                    f"dream-failed:{job_id}:{attempts}",
                ),
            )
        return DreamJobResult(job_id, status, attempts, available_at)

    def search_sources(self, query: str, limit: int = 10) -> list[SourceSearchResult]:
        if limit < 1:
            raise ValueError("limit must be positive")
        terms = re.findall(r"[A-Za-z0-9_]+|[\u3040-\u30ff\u3400-\u9fff]+", query)
        if not terms:
            return []
        match_query = " AND ".join('"' + term.replace('"', '""') + '"' for term in terms)
        rows = self.connection.execute(
            "SELECT c.source_id, d.source_uri, d.title, c.chunk_id, c.ordinal, c.content, "
            "bm25(source_chunk_search) AS score "
            "FROM source_chunk_search f "
            "JOIN source_chunks c ON c.chunk_id = f.chunk_id "
            "JOIN source_documents d ON d.source_id = c.source_id "
            "WHERE source_chunk_search MATCH ? AND d.source_state = 'active' "
            "ORDER BY score LIMIT ?",
            (match_query, limit),
        ).fetchall()
        return [
            SourceSearchResult(
                source_id=str(row[0]),
                source_uri=str(row[1]),
                title=str(row[2]),
                chunk_id=str(row[3]),
                ordinal=int(row[4]),
                content=str(row[5]),
                score=float(row[6]),
            )
            for row in rows
        ]

    def list_sources(self, limit: int = 100) -> list[SourceListEntry]:
        if limit < 1:
            raise ValueError("limit must be positive")
        rows = self.connection.execute(
            "SELECT d.source_id, d.source_uri, d.title, d.media_type, d.source_state, "
            "d.ingested_at, COUNT(c.chunk_id) FROM source_documents d "
            "LEFT JOIN source_chunks c ON c.source_id = d.source_id "
            "GROUP BY d.source_id ORDER BY d.ingested_at DESC, d.source_id LIMIT ?",
            (limit,),
        ).fetchall()
        return [
            SourceListEntry(
                source_id=str(row[0]),
                source_uri=str(row[1]),
                title=str(row[2]),
                media_type=str(row[3]),
                source_state=str(row[4]),
                ingested_at=str(row[5]),
                chunk_count=int(row[6]),
            )
            for row in rows
        ]

    def add_fact_candidate(
        self,
        source_id: str,
        statement: str,
        evidence_quote: str,
        *,
        language: str,
        memory_type: str = "fact",
        confidence: float = 0.5,
    ) -> FactWriteResult:
        """Store a source-grounded candidate without treating entailment as verified."""
        statement = statement.strip()
        evidence_quote = evidence_quote.strip()
        if not statement or not evidence_quote or not language.strip():
            raise ValueError("statement, evidence_quote, and language are required")
        if not 0 <= confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        if memory_type not in {"fact", "preference", "episode", "inference"}:
            raise ValueError("unsupported memory_type")
        source = self.connection.execute(
            "SELECT raw_content FROM source_documents WHERE source_id = ? AND source_state = 'active'",
            (source_id,),
        ).fetchone()
        if source is None:
            raise ValueError("source is missing or inactive")
        offset = str(source[0]).find(evidence_quote)
        if offset < 0:
            raise ValueError("evidence_quote must appear verbatim in the source")
        digest = hashlib.sha256(
            f"{source_id}\0{statement}\0{evidence_quote}".encode("utf-8")
        ).hexdigest()[:32]
        existing = self.connection.execute(
            "SELECT fact_id FROM fact_evidence WHERE fact_id = ? AND source_id = ? AND quote = ?",
            (digest, source_id, evidence_quote),
        ).fetchone()
        if existing:
            evidence_id = hashlib.sha256(f"evidence:{digest}:{source_id}".encode()).hexdigest()[:32]
            return FactWriteResult(digest, evidence_id, "pending_review", False)
        now = _utc_now()
        evidence_id = hashlib.sha256(f"evidence:{digest}:{source_id}".encode()).hexdigest()[:32]
        with self.connection:
            self.connection.execute(
                "INSERT INTO memory_facts "
                "(fact_id, statement, language, memory_type, status, confidence, recorded_at) "
                "VALUES (?, ?, ?, ?, 'pending_review', ?, ?)",
                (digest, statement, language.strip(), memory_type, confidence, now),
            )
            self.connection.execute(
                "INSERT INTO fact_evidence "
                "(evidence_id, fact_id, source_id, quote, start_offset, end_offset, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    evidence_id,
                    digest,
                    source_id,
                    evidence_quote,
                    offset,
                    offset + len(evidence_quote),
                    now,
                ),
            )
            self.connection.execute(
                "INSERT INTO memory_events "
                "(event_id, fact_id, source_id, event_type, occurred_at, payload_json, idempotency_key) "
                "VALUES (?, ?, ?, 'fact_asserted', ?, ?, ?)",
                (
                    hashlib.sha256(f"event:fact:{digest}".encode()).hexdigest()[:32],
                    digest,
                    source_id,
                    now,
                    json.dumps({"status": "pending_review"}),
                    f"fact-asserted:{digest}",
                ),
            )
        return FactWriteResult(digest, evidence_id, "pending_review", True)

    def review_fact(self, fact_id: str, *, accepted: bool, reviewer: str, reason: str = "") -> None:
        reviewer = reviewer.strip()
        if not reviewer:
            raise ValueError("reviewer is required")
        row = self.connection.execute(
            "SELECT source_id FROM fact_evidence WHERE fact_id = ? ORDER BY evidence_id LIMIT 1",
            (fact_id,),
        ).fetchone()
        status = self.connection.execute(
            "SELECT status FROM memory_facts WHERE fact_id = ?", (fact_id,)
        ).fetchone()
        if status is None:
            raise ValueError("fact does not exist")
        if status[0] != "pending_review":
            raise ValueError("only pending_review facts can be reviewed")
        now = _utc_now()
        next_status = "active" if accepted else "rejected"
        payload = json.dumps(
            {"accepted": accepted, "reviewer": reviewer, "reason": reason.strip()},
            ensure_ascii=False,
        )
        with self.connection:
            self.connection.execute(
                "UPDATE memory_facts SET status = ? WHERE fact_id = ?",
                (next_status, fact_id),
            )
            self.connection.execute(
                "INSERT INTO memory_events "
                "(event_id, fact_id, source_id, event_type, occurred_at, payload_json, idempotency_key) "
                "VALUES (?, ?, ?, 'fact_reviewed', ?, ?, ?)",
                (
                    hashlib.sha256(f"event:fact-review:{fact_id}".encode()).hexdigest()[:32],
                    fact_id,
                    row[0] if row else None,
                    now,
                    payload,
                    f"fact-reviewed:{fact_id}",
                ),
            )

    def save_localization(self, fact_id: str, locale: str, statement: str) -> None:
        locale = locale.strip()
        statement = statement.strip()
        if not locale or not statement:
            raise ValueError("locale and statement are required")
        fact = self.connection.execute(
            "SELECT status FROM memory_facts WHERE fact_id = ?", (fact_id,)
        ).fetchone()
        if fact is None:
            raise ValueError("fact does not exist")
        if fact[0] != "active":
            raise ValueError("localization can only be added to an active fact")
        with self.connection:
            self.connection.execute(
                "INSERT INTO memory_localizations "
                "(fact_id, locale, statement, review_status, created_at) "
                "VALUES (?, ?, ?, 'pending', ?)",
                (fact_id, locale, statement, _utc_now()),
            )

    def review_localization(
        self, fact_id: str, locale: str, *, approved: bool, reviewer: str, reason: str = ""
    ) -> None:
        locale = locale.strip()
        reviewer = reviewer.strip()
        if not locale or not reviewer:
            raise ValueError("locale and reviewer are required")
        row = self.connection.execute(
            "SELECT review_status FROM memory_localizations WHERE fact_id = ? AND locale = ?",
            (fact_id, locale),
        ).fetchone()
        if row is None:
            raise ValueError("localization does not exist")
        if row[0] != "pending":
            raise ValueError("only pending localizations can be reviewed")
        review_status = "approved" if approved else "rejected"
        payload = json.dumps(
            {
                "kind": "localization_reviewed",
                "locale": locale,
                "approved": approved,
                "reviewer": reviewer,
                "reason": reason.strip(),
            },
            ensure_ascii=False,
        )
        now = _utc_now()
        with self.connection:
            self.connection.execute(
                "UPDATE memory_localizations SET review_status = ?, reviewer_note = ? "
                "WHERE fact_id = ? AND locale = ?",
                (review_status, reason.strip(), fact_id, locale),
            )
            self.connection.execute(
                "INSERT INTO memory_events "
                "(event_id, fact_id, event_type, occurred_at, payload_json, idempotency_key) "
                "VALUES (?, ?, 'fact_reviewed', ?, ?, ?)",
                (
                    hashlib.sha256(
                        f"event:localization-review:{fact_id}:{locale}".encode()
                    ).hexdigest()[:32],
                    fact_id,
                    now,
                    payload,
                    f"localization-reviewed:{fact_id}:{locale}",
                ),
            )

    def get_recall_statement(self, fact_id: str, locale: str) -> str:
        row = self.connection.execute(
            "SELECT f.statement, f.language, f.status, l.statement, l.review_status "
            "FROM memory_facts f LEFT JOIN memory_localizations l "
            "ON l.fact_id = f.fact_id AND l.locale = ? WHERE f.fact_id = ?",
            (locale, fact_id),
        ).fetchone()
        if row is None or row[2] != "active":
            raise ValueError("fact is not active for recall")
        if str(row[1]).casefold() == locale.casefold():
            return str(row[0])
        if row[4] != "approved":
            raise ValueError("localization is not approved")
        return str(row[3])

    def resolve_entity(
        self, canonical_name: str, entity_type: str, *, language: str = ""
    ) -> EntityWriteResult:
        canonical_name = canonical_name.strip()
        allowed_types = {
            "person",
            "organization",
            "product",
            "project",
            "place",
            "event",
            "concept",
            "other",
        }
        if not canonical_name:
            raise ValueError("canonical_name is required")
        if entity_type not in allowed_types:
            raise ValueError("unsupported entity_type")
        normalized = _normalize_entity_name(canonical_name)
        matches = self.connection.execute(
            "SELECT DISTINCT e.entity_id, e.canonical_name, e.entity_type "
            "FROM entity_aliases a JOIN entities e ON e.entity_id = a.entity_id "
            "WHERE a.normalized_alias = ? AND a.verified = 1",
            (normalized,),
        ).fetchall()
        typed_matches = [row for row in matches if row[2] == entity_type]
        if len(typed_matches) == 1:
            return EntityWriteResult(
                str(typed_matches[0][0]), str(typed_matches[0][1]), entity_type, False
            )
        if len(typed_matches) > 1 or (matches and not typed_matches):
            raise ValueError("ambiguous entity alias; manual resolution is required")

        entity_id = hashlib.sha256(f"entity:{entity_type}:{normalized}".encode()).hexdigest()[:32]
        now = _utc_now()
        with self.connection:
            self.connection.execute(
                "INSERT INTO entities (entity_id, canonical_name, entity_type, created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (entity_id, canonical_name, entity_type, now, now),
            )
            self.connection.execute(
                "INSERT INTO entity_aliases "
                "(entity_id, alias, language, normalized_alias, verified) "
                "VALUES (?, ?, ?, ?, 1)",
                (entity_id, canonical_name, language.strip(), normalized),
            )
        return EntityWriteResult(entity_id, canonical_name, entity_type, True)

    def register_entity_alias(
        self,
        entity_id: str,
        alias: str,
        *,
        reviewer: str,
        reason: str,
        language: str = "",
    ) -> EntityAliasWriteResult:
        alias = alias.strip()
        reviewer = reviewer.strip()
        reason = reason.strip()
        if not alias:
            raise ValueError("alias is required")
        if not reviewer:
            raise ValueError("reviewer is required")
        if not reason:
            raise ValueError("reason is required")
        entity = self.connection.execute(
            "SELECT entity_id FROM entities WHERE entity_id = ?", (entity_id,)
        ).fetchone()
        if entity is None:
            raise ValueError("entity does not exist")

        normalized = _normalize_entity_name(alias)
        existing = self.connection.execute(
            "SELECT entity_id FROM entity_aliases WHERE normalized_alias = ?",
            (normalized,),
        ).fetchall()
        if any(str(row[0]) != entity_id for row in existing):
            raise ValueError("alias already belongs to another entity")

        now = _utc_now()
        review_id = hashlib.sha256(
            f"entity-alias-review:{entity_id}:{normalized}:{reviewer}:{reason}".encode("utf-8")
        ).hexdigest()[:32]
        created = not existing
        with self.connection:
            if created:
                self.connection.execute(
                    "INSERT INTO entity_aliases "
                    "(entity_id, alias, language, normalized_alias, verified) "
                    "VALUES (?, ?, ?, ?, 1)",
                    (entity_id, alias, language.strip(), normalized),
                )
            else:
                self.connection.execute(
                    "UPDATE entity_aliases SET verified = 1 "
                    "WHERE entity_id = ? AND normalized_alias = ?",
                    (entity_id, normalized),
                )
            self.connection.execute(
                "INSERT OR IGNORE INTO entity_alias_reviews "
                "(review_id, entity_id, normalized_alias, reviewer, reason, reviewed_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (review_id, entity_id, normalized, reviewer, reason, now),
            )
            self.connection.execute(
                "UPDATE entities SET updated_at = ? WHERE entity_id = ?", (now, entity_id)
            )
        return EntityAliasWriteResult(entity_id, alias, normalized, created)

    def link_fact_entity(self, fact_id: str, entity_id: str, role: str) -> bool:
        if role not in {"subject", "object", "mentioned"}:
            raise ValueError("unsupported fact entity role")
        fact = self.connection.execute(
            "SELECT status FROM memory_facts WHERE fact_id = ?", (fact_id,)
        ).fetchone()
        if fact is None or fact[0] != "active":
            raise ValueError("entity links require an active fact")
        cursor = self.connection.execute(
            "INSERT OR IGNORE INTO fact_entities (fact_id, entity_id, role) VALUES (?, ?, ?)",
            (fact_id, entity_id, role),
        )
        return cursor.rowcount == 1

    def propose_fact_relation(
        self,
        from_fact_id: str,
        to_fact_id: str,
        relation_type: str,
        *,
        confidence: float,
        rationale: str = "",
    ) -> RelationWriteResult:
        relation_types = {"same", "extends", "updates", "contradicts", "derived_from"}
        if relation_type not in relation_types:
            raise ValueError("unsupported relation_type")
        if not 0 <= confidence <= 1:
            raise ValueError("confidence must be between 0 and 1")
        if relation_type == "same" and to_fact_id < from_fact_id:
            from_fact_id, to_fact_id = to_fact_id, from_fact_id
        if from_fact_id == to_fact_id:
            raise ValueError("a fact cannot be related to itself")
        active_ids = {
            str(row[0])
            for row in self.connection.execute(
                "SELECT fact_id FROM memory_facts WHERE fact_id IN (?, ?) AND status = 'active'",
                (from_fact_id, to_fact_id),
            )
        }
        if active_ids != {from_fact_id, to_fact_id}:
            raise ValueError("fact relations require two active facts")
        existing = self.connection.execute(
            "SELECT relation_id, status FROM fact_relations "
            "WHERE from_fact_id = ? AND to_fact_id = ? AND relation_type = ?",
            (from_fact_id, to_fact_id, relation_type),
        ).fetchone()
        if existing:
            return RelationWriteResult(str(existing[0]), str(existing[1]), False)
        relation_id = hashlib.sha256(
            f"relation:{from_fact_id}:{to_fact_id}:{relation_type}".encode()
        ).hexdigest()[:32]
        now = _utc_now()
        with self.connection:
            self.connection.execute(
                "INSERT INTO fact_relations "
                "(relation_id, from_fact_id, to_fact_id, relation_type, confidence, status, rationale, created_at) "
                "VALUES (?, ?, ?, ?, ?, 'proposed', ?, ?)",
                (
                    relation_id,
                    from_fact_id,
                    to_fact_id,
                    relation_type,
                    confidence,
                    rationale.strip(),
                    now,
                ),
            )
        return RelationWriteResult(relation_id, "proposed", True)

    def review_fact_relation(
        self, relation_id: str, *, accepted: bool, reviewer: str, reason: str = ""
    ) -> None:
        reviewer = reviewer.strip()
        if not reviewer:
            raise ValueError("reviewer is required")
        relation = self.connection.execute(
            "SELECT from_fact_id, status FROM fact_relations WHERE relation_id = ?",
            (relation_id,),
        ).fetchone()
        if relation is None:
            raise ValueError("relation does not exist")
        if relation[1] != "proposed":
            raise ValueError("only proposed relations can be reviewed")
        now = _utc_now()
        next_status = "active" if accepted else "rejected"
        payload = json.dumps(
            {"accepted": accepted, "reviewer": reviewer, "reason": reason.strip()},
            ensure_ascii=False,
        )
        with self.connection:
            self.connection.execute(
                "UPDATE fact_relations SET status = ?, reviewed_at = ? WHERE relation_id = ?",
                (next_status, now, relation_id),
            )
            self.connection.execute(
                "INSERT INTO memory_events "
                "(event_id, fact_id, event_type, occurred_at, payload_json, idempotency_key) "
                "VALUES (?, ?, 'relation_reviewed', ?, ?, ?)",
                (
                    hashlib.sha256(f"event:relation-review:{relation_id}".encode()).hexdigest()[
                        :32
                    ],
                    str(relation[0]),
                    now,
                    payload,
                    f"relation-reviewed:{relation_id}",
                ),
            )

    def supersede_fact(
        self,
        old_fact_id: str,
        new_fact_id: str,
        *,
        effective_at: str,
        reviewer: str,
        rationale: str = "",
    ) -> bool:
        effective_at = _normalize_timestamp(effective_at)
        reviewer = reviewer.strip()
        rationale = rationale.strip()
        if not reviewer:
            raise ValueError("reviewer is required")
        if old_fact_id == new_fact_id:
            raise ValueError("a fact cannot supersede itself")
        rows = self.connection.execute(
            "SELECT fact_id, status, valid_from, valid_to, supersedes_fact_id "
            "FROM memory_facts WHERE fact_id IN (?, ?)",
            (old_fact_id, new_fact_id),
        ).fetchall()
        by_id = {str(row[0]): row for row in rows}
        if old_fact_id not in by_id or new_fact_id not in by_id:
            raise ValueError("both facts must exist")
        old, new = by_id[old_fact_id], by_id[new_fact_id]
        if old[1] == "superseded" and new[4] == old_fact_id and old[3] == effective_at:
            return False
        if old[1] != "active" or new[1] != "active":
            raise ValueError("superseding requires two active facts")
        if new[4] is not None:
            raise ValueError("new fact already supersedes another fact")
        if old[2] is not None and _normalize_timestamp(str(old[2])) > effective_at:
            raise ValueError("effective_at precedes the old fact's valid_from")
        if new[2] is not None and _normalize_timestamp(str(new[2])) != effective_at:
            raise ValueError("effective_at must match the new fact's existing valid_from")

        now = _utc_now()
        relation_id = hashlib.sha256(
            f"relation:{new_fact_id}:{old_fact_id}:updates".encode()
        ).hexdigest()[:32]
        event_id = hashlib.sha256(f"event:fact-superseded:{old_fact_id}".encode()).hexdigest()[:32]
        payload = json.dumps(
            {
                "old_fact_id": old_fact_id,
                "new_fact_id": new_fact_id,
                "effective_at": effective_at,
                "reviewer": reviewer,
                "rationale": rationale,
            },
            ensure_ascii=False,
        )
        with self.connection:
            self.connection.execute(
                "UPDATE memory_facts SET status = 'superseded', valid_to = ? WHERE fact_id = ?",
                (effective_at, old_fact_id),
            )
            self.connection.execute(
                "UPDATE memory_facts SET valid_from = ?, supersedes_fact_id = ? WHERE fact_id = ?",
                (effective_at, old_fact_id, new_fact_id),
            )
            relation = self.connection.execute(
                "SELECT relation_id, status FROM fact_relations "
                "WHERE from_fact_id = ? AND to_fact_id = ? AND relation_type = 'updates'",
                (new_fact_id, old_fact_id),
            ).fetchone()
            if relation is None:
                self.connection.execute(
                    "INSERT INTO fact_relations "
                    "(relation_id, from_fact_id, to_fact_id, relation_type, confidence, status, rationale, created_at, reviewed_at) "
                    "VALUES (?, ?, ?, 'updates', 1.0, 'active', ?, ?, ?)",
                    (relation_id, new_fact_id, old_fact_id, rationale, now, now),
                )
            elif relation[1] == "proposed":
                self.connection.execute(
                    "UPDATE fact_relations SET status = 'active', confidence = 1.0, rationale = ?, reviewed_at = ? "
                    "WHERE relation_id = ?",
                    (rationale, now, relation[0]),
                )
            elif relation[1] != "active":
                raise ValueError("an existing updates relation was rejected or superseded")
            self.connection.execute(
                "INSERT INTO memory_events "
                "(event_id, fact_id, event_type, occurred_at, payload_json, idempotency_key) "
                "VALUES (?, ?, 'fact_superseded', ?, ?, ?)",
                (event_id, old_fact_id, now, payload, f"fact-superseded:{old_fact_id}"),
            )
        return True

    def forget_fact(
        self, fact_id: str, *, reviewer: str, reason: str, forgotten_at: str | None = None
    ) -> bool:
        reviewer = reviewer.strip()
        reason = reason.strip()
        if not reviewer or not reason:
            raise ValueError("reviewer and reason are required")
        occurred_at = _normalize_timestamp(forgotten_at or _utc_now())
        row = self.connection.execute(
            "SELECT status, source_id FROM memory_facts f LEFT JOIN fact_evidence e "
            "ON e.fact_id = f.fact_id WHERE f.fact_id = ? ORDER BY e.evidence_id LIMIT 1",
            (fact_id,),
        ).fetchone()
        if row is None:
            raise ValueError("fact does not exist")
        if row[0] == "forgotten":
            return False
        if row[0] in {"rejected"}:
            raise ValueError("rejected facts cannot be forgotten")
        payload = json.dumps({"reviewer": reviewer, "reason": reason}, ensure_ascii=False)
        event_id = hashlib.sha256(f"event:fact-forgotten:{fact_id}".encode()).hexdigest()[:32]
        with self.connection:
            self.connection.execute(
                "UPDATE memory_facts SET status = 'forgotten' WHERE fact_id = ?", (fact_id,)
            )
            self.connection.execute(
                "INSERT INTO memory_events "
                "(event_id, fact_id, source_id, event_type, occurred_at, payload_json, idempotency_key) "
                "VALUES (?, ?, ?, 'fact_forgotten', ?, ?, ?)",
                (event_id, fact_id, row[1], occurred_at, payload, f"fact-forgotten:{fact_id}"),
            )
        return True

    def list_recall_facts(self, locale: str, *, as_of: str | None = None) -> list[RecallFact]:
        locale = locale.strip()
        if not locale:
            raise ValueError("locale is required")
        timestamp = _normalize_timestamp(as_of) if as_of else _utc_now()
        statuses = "('active', 'superseded')" if as_of else "('active')"
        rows = self.connection.execute(
            "SELECT f.fact_id, f.statement, f.language, f.memory_type, f.confidence, "
            "f.valid_from, f.valid_to, l.statement, l.review_status "
            "FROM memory_facts f LEFT JOIN memory_localizations l "
            "ON l.fact_id = f.fact_id AND l.locale = ? "
            f"WHERE f.status IN {statuses} "
            "AND (f.valid_from IS NULL OR f.valid_from <= ?) "
            "AND (f.valid_to IS NULL OR f.valid_to > ?) "
            "ORDER BY f.recorded_at DESC, f.fact_id",
            (locale, timestamp, timestamp),
        ).fetchall()
        locale_language = locale.replace("_", "-").split("-")[0].casefold()
        results: list[RecallFact] = []
        for row in rows:
            language = str(row[2])
            if language.replace("_", "-").split("-")[0].casefold() == locale_language:
                statement = str(row[1])
            elif row[8] == "approved":
                statement = str(row[7])
            else:
                continue
            results.append(
                RecallFact(
                    fact_id=str(row[0]),
                    statement=statement,
                    language=language,
                    memory_type=str(row[3]),
                    confidence=float(row[4]),
                    valid_from=str(row[5]) if row[5] is not None else None,
                    valid_to=str(row[6]) if row[6] is not None else None,
                )
            )
        return results

    def search_recall_facts(
        self, query: str, locale: str, *, limit: int = 10, as_of: str | None = None
    ) -> list[RecallFact]:
        locale = locale.strip()
        if not locale:
            raise ValueError("locale is required")
        if limit < 1:
            raise ValueError("limit must be positive")
        terms = re.findall(r"[A-Za-z0-9_]+|[\u3040-\u30ff\u3400-\u9fff]+", query)
        if not terms:
            return []
        match_query = " AND ".join('"' + term.replace('"', '""') + '"' for term in terms)
        timestamp = _normalize_timestamp(as_of) if as_of else _utc_now()
        statuses = "('active', 'superseded')" if as_of else "('active')"
        rows = self.connection.execute(
            "SELECT f.fact_id, f.statement, f.language, f.memory_type, f.confidence, "
            "f.valid_from, f.valid_to, d.source_uri, d.title, e.quote, l.statement, "
            "l.review_status, bm25(source_chunk_search) AS score "
            "FROM source_chunk_search s "
            "JOIN source_chunks c ON c.chunk_id = s.chunk_id "
            "JOIN source_documents d ON d.source_id = c.source_id "
            "JOIN fact_evidence e ON e.source_id = d.source_id "
            "JOIN memory_facts f ON f.fact_id = e.fact_id "
            "LEFT JOIN memory_localizations l ON l.fact_id = f.fact_id AND l.locale = ? "
            "WHERE source_chunk_search MATCH ? AND d.source_state = 'active' "
            f"AND f.status IN {statuses} "
            "AND (f.valid_from IS NULL OR f.valid_from <= ?) "
            "AND (f.valid_to IS NULL OR f.valid_to > ?) "
            "ORDER BY score, f.confidence DESC",
            (locale, match_query, timestamp, timestamp),
        ).fetchall()
        locale_language = locale.replace("_", "-").split("-")[0].casefold()
        results: dict[str, RecallFact] = {}
        for row in rows:
            language = str(row[2])
            if language.replace("_", "-").split("-")[0].casefold() == locale_language:
                statement = str(row[1])
            elif row[11] == "approved":
                statement = str(row[10])
            else:
                continue
            fact_id = str(row[0])
            results.setdefault(
                fact_id,
                RecallFact(
                    fact_id=fact_id,
                    statement=statement,
                    language=language,
                    memory_type=str(row[3]),
                    confidence=float(row[4]),
                    valid_from=str(row[5]) if row[5] is not None else None,
                    valid_to=str(row[6]) if row[6] is not None else None,
                    source_uri=str(row[7]),
                    source_title=str(row[8]),
                    evidence_quote=str(row[9]),
                ),
            )
        return list(results.values())[:limit]

    def erase_source(self, source_id: str) -> SourceEraseResult:
        row = self.connection.execute(
            "SELECT source_uri FROM source_documents WHERE source_id = ?", (source_id,)
        ).fetchone()
        if row is None:
            raise ValueError("source does not exist")
        source_uri = str(row[0])
        source_ids = [
            str(item[0])
            for item in self.connection.execute(
                "SELECT source_id FROM source_documents WHERE source_uri = ?", (source_uri,)
            )
        ]
        placeholders = ",".join("?" for _ in source_ids)
        affected_fact_ids = [
            str(item[0])
            for item in self.connection.execute(
                "WITH RECURSIVE affected(fact_id) AS ("
                f"SELECT DISTINCT fact_id FROM fact_evidence WHERE source_id IN ({placeholders}) "
                "UNION "
                "SELECT r.from_fact_id FROM fact_relations r "
                "JOIN affected a ON r.to_fact_id = a.fact_id "
                "WHERE r.relation_type = 'derived_from'"
                ") SELECT fact_id FROM affected",
                source_ids,
            )
        ]
        fact_count = len(affected_fact_ids)
        relation_count = 0
        if affected_fact_ids:
            fact_placeholders = ",".join("?" for _ in affected_fact_ids)
            relation_count = int(
                self.connection.execute(
                    "SELECT COUNT(*) FROM fact_relations "
                    f"WHERE from_fact_id IN ({fact_placeholders}) "
                    f"OR to_fact_id IN ({fact_placeholders})",
                    [*affected_fact_ids, *affected_fact_ids],
                ).fetchone()[0]
            )
        job_count = int(
            self.connection.execute(
                "SELECT COUNT(*) FROM dream_jobs WHERE job_key IN ("
                + ",".join("?" for _ in source_ids)
                + ")",
                [f"source:{item}" for item in source_ids],
            ).fetchone()[0]
        )
        now = _utc_now()
        self._erase_authorized = True
        try:
            with self.connection:
                fact_placeholders = ",".join("?" for _ in affected_fact_ids)
                if affected_fact_ids:
                    self.connection.execute(
                        "DELETE FROM memory_events "
                        f"WHERE source_id IN ({placeholders}) OR fact_id IN ({fact_placeholders})",
                        [*source_ids, *affected_fact_ids],
                    )
                    self.connection.execute(
                        "UPDATE memory_facts SET supersedes_fact_id = NULL "
                        f"WHERE supersedes_fact_id IN ({fact_placeholders}) "
                        f"AND fact_id NOT IN ({fact_placeholders})",
                        [*affected_fact_ids, *affected_fact_ids],
                    )
                    self.connection.execute(
                        f"DELETE FROM memory_facts WHERE fact_id IN ({fact_placeholders})",
                        affected_fact_ids,
                    )
                else:
                    self.connection.execute(
                        f"DELETE FROM memory_events WHERE source_id IN ({placeholders})",
                        source_ids,
                    )
                self.connection.execute(
                    "DELETE FROM dream_jobs WHERE job_key IN ("
                    + ",".join("?" for _ in source_ids)
                    + ")",
                    [f"source:{item}" for item in source_ids],
                )
                self.connection.execute(
                    f"DELETE FROM source_documents WHERE source_id IN ({placeholders})", source_ids
                )
                self.connection.execute(
                    "DELETE FROM entities WHERE NOT EXISTS ("
                    "SELECT 1 FROM fact_entities WHERE fact_entities.entity_id = entities.entity_id)"
                )
                self.connection.execute(
                    "INSERT INTO memory_events "
                    "(event_id, event_type, occurred_at, payload_json) "
                    "VALUES (?, 'source_deleted', ?, '{\"erased\":true}')",
                    (uuid.uuid4().hex, now),
                )
        finally:
            self._erase_authorized = False
        return SourceEraseResult(
            source_count=len(source_ids),
            fact_count=fact_count,
            relation_count=relation_count,
            dream_job_count=job_count,
        )

    def close(self) -> None:
        self.connection.close()

    def __enter__(self) -> MemoryStore:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()
