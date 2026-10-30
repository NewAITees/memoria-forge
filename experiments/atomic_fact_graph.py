"""Minimal evidence-grounded fact graph used by the local memory experiment."""

from __future__ import annotations

import html
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType


RELATIONS = frozenset({"same", "extends", "updates", "contradicts"})
NUMBER_WORDS = frozenset(
    {
        "zero",
        "one",
        "two",
        "three",
        "four",
        "five",
        "six",
        "seven",
        "eight",
        "nine",
        "ten",
        "hundred",
        "thousand",
        "million",
    }
)
STOPWORDS = frozenset(
    {
        "a",
        "an",
        "and",
        "as",
        "at",
        "by",
        "for",
        "from",
        "in",
        "is",
        "of",
        "on",
        "or",
        "the",
        "to",
        "was",
        "were",
        "with",
    }
)


@dataclass(frozen=True)
class SourceDocument:
    document_id: str
    title: str
    url: str
    content: str


@dataclass(frozen=True)
class Fact:
    fact_id: str
    statement: str
    evidence_quote: str
    source_document_id: str
    confidence: float
    status: str = "active"


def normalize_evidence(text: str) -> str:
    """Normalize layout without changing words, so quotes remain auditable."""
    without_tags = re.sub(r"<[^>]+>", " ", html.unescape(text))
    return re.sub(r"\s+", " ", without_tags).strip()


def validate_fact(fact: Fact, source: SourceDocument) -> bool:
    if fact.source_document_id != source.document_id:
        return False
    quote = normalize_evidence(fact.evidence_quote)
    return bool(quote) and quote in normalize_evidence(source.content)


def _tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z0-9_-]*|\d+(?:[.,]\d+)*%?", text)


def unsupported_critical_tokens(statement: str, evidence_quote: str) -> set[str]:
    """Find objective identifiers in a claim that its quoted evidence lacks."""
    evidence = {token.casefold() for token in _tokens(evidence_quote)}
    unsupported: set[str] = set()
    for index, token in enumerate(_tokens(statement)):
        folded = token.casefold()
        is_number = any(character.isdigit() for character in token) or folded in NUMBER_WORDS
        is_acronym = len(token) > 1 and token.isupper()
        is_named = index > 0 and token[0].isupper() and folded not in STOPWORDS
        if (is_number or is_acronym or is_named) and folded not in evidence:
            unsupported.add(folded)
    return unsupported


def _salient_tokens(text: str) -> set[str]:
    return {
        token.casefold()
        for token in _tokens(text)
        if len(token) >= 3 and token.casefold() not in STOPWORDS
    }


def _named_tokens(text: str) -> set[str]:
    return {
        token.casefold()
        for index, token in enumerate(_tokens(text))
        if index > 0 and token[0].isupper() and token.casefold() not in STOPWORDS
    }


def candidate_relation_pairs(facts: list[Fact]) -> list[tuple[Fact, Fact]]:
    """Bound relation review to cross-document facts with a shared subject signal."""
    pairs: list[tuple[Fact, Fact]] = []
    for index, left in enumerate(facts):
        for right in facts[index + 1 :]:
            if left.source_document_id == right.source_document_id:
                continue
            left_words, right_words = _salient_tokens(left.statement), _salient_tokens(
                right.statement
            )
            common = left_words & right_words
            shared_name = _named_tokens(left.statement) & _named_tokens(right.statement)
            union = left_words | right_words
            similarity = len(common) / len(union) if union else 0.0
            non_name_overlap = common - shared_name
            if (shared_name and non_name_overlap) or (len(common) >= 2 and similarity >= 0.2):
                pairs.append((left, right))
    return pairs


class FactStore:
    def __init__(self, path: Path) -> None:
        self.db = sqlite3.connect(path)
        self.db.executescript(
            """
            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                content TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS facts (
                fact_id TEXT PRIMARY KEY,
                statement TEXT NOT NULL,
                evidence_quote TEXT NOT NULL,
                source_document_id TEXT NOT NULL,
                confidence REAL NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (source_document_id) REFERENCES documents(document_id)
            );
            CREATE TABLE IF NOT EXISTS fact_relations (
                from_fact_id TEXT NOT NULL,
                to_fact_id TEXT NOT NULL,
                relation TEXT NOT NULL,
                confidence REAL NOT NULL,
                PRIMARY KEY (from_fact_id, to_fact_id, relation)
            );
            CREATE TABLE IF NOT EXISTS rejected_facts (
                fact_id TEXT,
                statement TEXT,
                evidence_quote TEXT,
                source_document_id TEXT,
                reason TEXT NOT NULL
            );
            """
        )
        self.db.commit()

    def __enter__(self) -> FactStore:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.db.close()

    def add_source(self, source: SourceDocument) -> None:
        self.db.execute(
            "INSERT OR REPLACE INTO documents VALUES (?, ?, ?, ?)",
            (source.document_id, source.title, source.url, source.content),
        )
        self.db.commit()

    def add_fact(self, fact: Fact) -> bool:
        row = self.db.execute(
            "SELECT document_id, title, url, content FROM documents WHERE document_id = ?",
            (fact.source_document_id,),
        ).fetchone()
        source = SourceDocument(*row) if row else None
        if source is None or not validate_fact(fact, source):
            self.db.execute(
                "INSERT INTO rejected_facts VALUES (?, ?, ?, ?, ?)",
                (
                    fact.fact_id,
                    fact.statement,
                    fact.evidence_quote,
                    fact.source_document_id,
                    "evidence_quote_not_found",
                ),
            )
            self.db.commit()
            return False
        self.db.execute(
            "INSERT OR REPLACE INTO facts VALUES (?, ?, ?, ?, ?, ?)",
            (
                fact.fact_id,
                fact.statement,
                fact.evidence_quote,
                fact.source_document_id,
                fact.confidence,
                fact.status,
            ),
        )
        self.db.commit()
        return True

    def add_relation(
        self, from_fact_id: str, to_fact_id: str, relation: str, confidence: float
    ) -> None:
        if relation not in RELATIONS:
            raise ValueError(f"unsupported relation: {relation}")
        self.db.execute(
            "INSERT OR REPLACE INTO fact_relations VALUES (?, ?, ?, ?)",
            (from_fact_id, to_fact_id, relation, confidence),
        )
        self.db.commit()

    def fact_count(self) -> int:
        return int(self.db.execute("SELECT COUNT(*) FROM facts").fetchone()[0])

    def rejected_count(self) -> int:
        return int(self.db.execute("SELECT COUNT(*) FROM rejected_facts").fetchone()[0])

    def relation_count(self) -> int:
        return int(self.db.execute("SELECT COUNT(*) FROM fact_relations").fetchone()[0])

    def active_facts(self) -> list[Fact]:
        rows = self.db.execute(
            "SELECT fact_id, statement, evidence_quote, source_document_id, confidence, status "
            "FROM facts WHERE status = 'active' ORDER BY fact_id"
        ).fetchall()
        return [Fact(*row) for row in rows]
