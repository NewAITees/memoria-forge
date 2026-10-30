"""Evidence-grounded atomic facts for new Wiki pages.

Design: docs/設計_v2幾何エンジン_2026-07-30.md
Related: wiki_agent.StateDB, wiki_agent.Ollama, research.deep_research
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import sqlite3
from dataclasses import dataclass, replace
from typing import Any, Iterable, cast


# wiki_agent fetches up to config.max_pages_fetched (5) sources, each snippet
# capped at 12000 chars, so the evidence block can reach ~60000 chars. num_ctx=16384
# tokens comfortably covers that; a smaller cutoff here silently dropped later
# sources from the model's view regardless of num_ctx.
MAX_EVIDENCE_MATERIAL_CHARS = 64000

FACT_EXTRACTION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "facts": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "statement": {"type": "string"},
                    "evidence_quote": {"type": "string"},
                    "source_id": {"type": "string"},
                    "confidence": {"type": "number"},
                },
                "required": [
                    "statement",
                    "evidence_quote",
                    "source_id",
                    "confidence",
                ],
            },
        }
    },
    "required": ["facts"],
}

FACT_REVIEW_SCHEMA: dict[str, Any] = {
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

FACT_LOCALIZATION_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "translations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "fact_id": {"type": "string"},
                    "statement_ja": {"type": "string"},
                },
                "required": ["fact_id", "statement_ja"],
            },
        }
    },
    "required": ["translations"],
}

GROUNDED_PAGE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "overview": {"type": "string"},
        "implications": {"type": "string"},
        "implication_fact_ids": {"type": "array", "items": {"type": "string"}},
        "uncertainties": {"type": "string"},
    },
    "required": ["title", "overview", "implications", "implication_fact_ids", "uncertainties"],
}

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
GROUNDED_SECTIONS = (
    "何が分かったか",
    "確認できた事実",
    "それが意味すること",
    "まだ分からないこと",
    "出典",
)


@dataclass(frozen=True)
class AtomicFact:
    fact_id: str
    statement: str
    evidence_quote: str
    source_url: str
    source_title: str
    confidence: float
    statement_ja: str = ""


def normalize_evidence(text: str) -> str:
    without_tags = re.sub(r"<[^>]+>", " ", html.unescape(text))
    return re.sub(r"\s+", " ", without_tags).strip()


def _normalized_source_spans(source: str) -> tuple[str, list[tuple[int, int]]]:
    entity_pattern = re.compile(r"&(?:#(?:[xX][0-9a-fA-F]+|[0-9]+)|[A-Za-z][A-Za-z0-9]+);?")
    decoded_chars: list[str] = []
    decoded_spans: list[tuple[int, int]] = []
    index = 0
    while index < len(source):
        entity = entity_pattern.match(source, index) if source[index] == "&" else None
        if entity is not None:
            raw_entity = entity.group()
            decoded_entity = html.unescape(raw_entity)
            if decoded_entity != raw_entity:
                decoded_chars.extend(decoded_entity)
                decoded_spans.extend([(index, entity.end())] * len(decoded_entity))
                index = entity.end()
                continue
        decoded_chars.append(source[index])
        decoded_spans.append((index, index + 1))
        index += 1

    decoded = "".join(decoded_chars)
    tag_pattern = re.compile(r"<[^>]+>")
    stripped_chars: list[str] = []
    stripped_spans: list[tuple[int, int]] = []
    cursor = 0
    for tag in tag_pattern.finditer(decoded):
        for position in range(cursor, tag.start()):
            stripped_chars.append(decoded[position])
            stripped_spans.append(decoded_spans[position])
        stripped_chars.append(" ")
        stripped_spans.append((decoded_spans[tag.start()][0], decoded_spans[tag.end() - 1][1]))
        cursor = tag.end()
    for position in range(cursor, len(decoded)):
        stripped_chars.append(decoded[position])
        stripped_spans.append(decoded_spans[position])

    stripped = "".join(stripped_chars)
    normalized_chars: list[str] = []
    normalized_spans: list[tuple[int, int]] = []
    position = 0
    while position < len(stripped):
        if stripped[position].isspace():
            end = position + 1
            while end < len(stripped) and stripped[end].isspace():
                end += 1
            if normalized_chars:
                normalized_chars.append(" ")
                normalized_spans.append((stripped_spans[position][0], stripped_spans[end - 1][1]))
            position = end
            continue
        normalized_chars.append(stripped[position])
        normalized_spans.append(stripped_spans[position])
        position += 1
    if normalized_chars and normalized_chars[-1] == " ":
        normalized_chars.pop()
        normalized_spans.pop()
    return "".join(normalized_chars), normalized_spans


def canonicalize_evidence_quote(quote: str, source: str) -> str | None:
    candidate = quote.strip()
    if not candidate:
        return None
    if candidate in source:
        return candidate
    normalized_quote = normalize_evidence(candidate)
    normalized_source, spans = _normalized_source_spans(source)
    if normalized_source != normalize_evidence(source):
        return None
    start = normalized_source.find(normalized_quote)
    if not normalized_quote or start < 0:
        return None
    end = start + len(normalized_quote) - 1
    source_quote = source[spans[start][0] : spans[end][1]]
    return source_quote if normalize_evidence(source_quote) == normalized_quote else None


def _tokens(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z0-9_-]*|\d+(?:[.,]\d+)*%?", text)


def unsupported_critical_tokens(statement: str, evidence_quote: str) -> set[str]:
    evidence: set[str] = set()
    for token in _tokens(evidence_quote):
        folded = token.casefold()
        evidence.add(folded)
        if folded.endswith("s") and len(folded) > 3:
            evidence.add(folded[:-1])
    unsupported: set[str] = set()
    for index, token in enumerate(_tokens(statement)):
        folded = token.casefold()
        is_number = any(character.isdigit() for character in token) or folded in NUMBER_WORDS
        is_acronym = len(token) > 1 and token.isupper()
        is_named = index > 0 and token[0].isupper() and folded not in STOPWORDS
        if (is_number or is_acronym or is_named) and folded not in evidence:
            unsupported.add(folded)
    return unsupported


def validate_fact(fact: AtomicFact, material: str | dict[str, str], allowed_urls: set[str]) -> bool:
    return not fact_validation_issues(fact, material, allowed_urls)


def fact_validation_issues(
    fact: AtomicFact, material: str | dict[str, str], allowed_urls: set[str]
) -> list[str]:
    quote = fact.evidence_quote.strip()
    if isinstance(material, dict):
        source_material = material.get(fact.source_url, "")
    else:
        source_material = material
    issues: list[str] = []
    if not fact.statement:
        issues.append("empty_statement")
    if not quote:
        issues.append("empty_evidence_quote")
    if fact.source_url not in allowed_urls:
        issues.append("source_url_not_allowed")
    elif quote and quote not in source_material:
        issues.append("quote_not_found_in_cited_source")
    unsupported = unsupported_critical_tokens(
        fact.statement, normalize_evidence(fact.evidence_quote)
    )
    if unsupported:
        issues.append("unsupported_critical_tokens=" + ",".join(sorted(unsupported)))
    return issues


def evidence_material(research_context: str, sources: Iterable[Any]) -> str:
    blocks = [research_context.strip()]
    for index, source in enumerate(sources, start=1):
        blocks.append(
            f"SOURCE ID: source-{index}\nSOURCE TITLE: {source.title}\nSOURCE URL: {source.url}\n"
            f"SOURCE SNIPPET: {source.snippet}"
        )
    return "\n\n".join(block for block in blocks if block)


def _fact_id(source_url: str, statement: str, quote: str) -> str:
    value = "\n".join((source_url, statement, quote))
    return "fact-" + hashlib.sha256(value.encode()).hexdigest()[:16]


def extract_verified_facts(
    client: Any,
    title: str,
    research_context: str,
    sources: list[Any],
) -> tuple[list[AtomicFact], dict[str, str]]:
    sources = list(sources)
    material = evidence_material(research_context, sources)
    allowed_urls = {str(source.url) for source in sources}
    source_material = {str(source.url): str(source.snippet or "") for source in sources}
    sources_by_id = {f"source-{index}": source for index, source in enumerate(sources, start=1)}
    response = client.chat(
        "Extract only atomic facts that directly answer the requested Wiki page topic. Write each "
        "statement in the same language as its evidence quote; preserve the source's technical terms. "
        "Return JSON only. Copy evidence_quote verbatim from EVIDENCE. Select source_id exactly as "
        "shown; do not reproduce or invent a source URL. Each "
        "statement must express one fact and must not add conditions absent from its quote. Do not "
        "extract broad facts merely because they share a technology with the topic.",
        f"TOPIC: {title}\n\nEVIDENCE:\n{material[:MAX_EVIDENCE_MATERIAL_CHARS]}",
        FACT_EXTRACTION_SCHEMA,
    )
    verified: list[AtomicFact] = []
    verified_ids: set[str] = set()
    rejected: dict[str, str] = {}
    for index, item in enumerate(response.get("facts", [])):
        if not isinstance(item, dict):
            continue
        statement = str(item.get("statement", "")).strip()
        model_quote = str(item.get("evidence_quote", "")).strip()
        source_id = str(item.get("source_id", "")).strip()
        source = sources_by_id.get(source_id)
        if source is None:
            rejected[f"candidate-{index + 1}"] = "source_id_not_allowed"
            continue
        url = str(source.url)
        quote = (
            canonicalize_evidence_quote(model_quote, source_material.get(url, "")) or model_quote
        )
        fact = AtomicFact(
            fact_id=_fact_id(url, statement, quote),
            statement=statement,
            evidence_quote=quote,
            source_url=url,
            source_title=str(source.title),
            confidence=float(item.get("confidence", 0.0)),
        )
        issues = fact_validation_issues(fact, source_material, allowed_urls)
        if not issues and fact.fact_id in verified_ids:
            rejected[f"candidate-{index + 1}"] = "duplicate_fact"
        elif not issues:
            verified.append(fact)
            verified_ids.add(fact.fact_id)
        else:
            rejected[f"candidate-{index + 1}"] = ";".join(issues)
    return verified, rejected


def review_facts(reviewer: Any, facts: list[AtomicFact]) -> dict[str, Any]:
    payload = [
        {
            "fact_id": fact.fact_id,
            "claim": fact.statement,
            "quote": normalize_evidence(fact.evidence_quote),
        }
        for fact in facts
    ]
    return cast(
        dict[str, Any],
        reviewer.chat(
            "Review each fact independently. Accept only when the quote alone supports every condition, "
            "number, entity and causal qualification in the claim. Classify every supplied fact_id "
            "exactly once. Return JSON only.",
            json.dumps(payload, ensure_ascii=False),
            FACT_REVIEW_SCHEMA,
        ),
    )


def filter_reviewed_facts(
    facts: list[AtomicFact], review: dict[str, Any]
) -> tuple[list[AtomicFact], dict[str, str]]:
    known = {fact.fact_id for fact in facts}
    accepted_ids = {
        str(fact_id) for fact_id in review.get("accepted_fact_ids", []) if str(fact_id) in known
    }
    rejected: dict[str, str] = {}
    for item in review.get("rejected", []):
        if not isinstance(item, dict):
            continue
        fact_id = str(item.get("fact_id", ""))
        if fact_id in known and fact_id not in rejected:
            rejected[fact_id] = str(item.get("reason", "reviewer_rejected"))
    for fact_id in known - accepted_ids - set(rejected):
        rejected[fact_id] = "reviewer_omitted_fact"
    accepted = [
        fact for fact in facts if fact.fact_id in accepted_ids and fact.fact_id not in rejected
    ]
    return accepted, rejected


def localize_verified_facts(
    writer: Any, reviewer: Any, facts: list[AtomicFact]
) -> tuple[list[AtomicFact], dict[str, str]]:
    """Add Japanese display text after the source-language claim has been verified."""
    untranslated = [
        fact for fact in facts if not re.search(r"[\u3040-\u30ff\u3400-\u9fff]", fact.statement)
    ]
    localized = [
        replace(fact, statement_ja=fact.statement) for fact in facts if fact not in untranslated
    ]
    if not untranslated:
        return localized, {}

    payload = [
        {
            "fact_id": fact.fact_id,
            "statement": fact.statement,
            "evidence_quote": normalize_evidence(fact.evidence_quote),
        }
        for fact in untranslated
    ]
    response = writer.chat(
        "Translate each verified factual statement into natural Japanese for display. Preserve "
        "every meaning, qualification, negation, number and entity. Do not add explanation or "
        "information. The evidence quote is for context only; keep it unchanged and do not translate it. "
        "Return one translation for every supplied fact_id and JSON only.",
        json.dumps(payload, ensure_ascii=False),
        FACT_LOCALIZATION_SCHEMA,
    )
    translations: dict[str, str] = {}
    for item in response.get("translations", []):
        if not isinstance(item, dict):
            continue
        fact_id = str(item.get("fact_id", ""))
        if fact_id not in {fact.fact_id for fact in untranslated} or fact_id in translations:
            continue
        translations[fact_id] = str(item.get("statement_ja", "")).strip()

    candidates: list[AtomicFact] = []
    rejected: dict[str, str] = {}
    for fact in untranslated:
        statement_ja = translations.get(fact.fact_id, "")
        if not statement_ja:
            rejected[fact.fact_id] = "localization_missing"
            continue
        if not re.search(r"[\u3040-\u30ff\u3400-\u9fff]", statement_ja):
            rejected[fact.fact_id] = "localization_not_japanese"
            continue
        source_numbers = sorted(
            token for token in _tokens(fact.statement) if any(c.isdigit() for c in token)
        )
        display_numbers = sorted(
            token for token in _tokens(statement_ja) if any(c.isdigit() for c in token)
        )
        if source_numbers != display_numbers:
            rejected[fact.fact_id] = "localization_changed_numeric_tokens"
            continue
        candidates.append(replace(fact, statement_ja=statement_ja))

    if candidates:
        review_payload = [
            {
                "fact_id": fact.fact_id,
                "source_language_statement": fact.statement,
                "japanese_display_statement": fact.statement_ja,
                "evidence_quote": normalize_evidence(fact.evidence_quote),
            }
            for fact in candidates
        ]
        review = reviewer.chat(
            "Review each Japanese display statement against the original source-language claim "
            "and its verbatim evidence quote. Accept only accurate translations that add no fact, "
            "drop no qualification, and preserve all numbers and entities. Classify every fact_id "
            "exactly once. Return JSON only.",
            json.dumps(review_payload, ensure_ascii=False),
            FACT_REVIEW_SCHEMA,
        )
        accepted, review_rejections = filter_reviewed_facts(candidates, review)
        localized.extend(accepted)
        rejected.update(review_rejections)
    localized_by_id = {fact.fact_id: fact for fact in localized}
    return [
        localized_by_id[fact.fact_id] for fact in facts if fact.fact_id in localized_by_id
    ], rejected


def render_grounded_page(
    title: str,
    facts: list[AtomicFact],
    implications: str,
    uncertainties: str,
    overview: str = "",
    implication_fact_ids: list[str] | None = None,
) -> str:
    # Defend against a duplicate fact_id reaching this function (seen live from a
    # stale pre-dedup extraction): never render the same fact twice.
    deduped: list[AtomicFact] = []
    seen_ids: set[str] = set()
    for fact in facts:
        if fact.fact_id in seen_ids:
            continue
        seen_ids.add(fact.fact_id)
        deduped.append(fact)
    facts = deduped

    overview = (
        overview.strip()
        or f"このページでは、調査資料から直接確認できた{len(facts)}件の事実を整理する。"
    )
    lines = [f"# {title}", "", "## 何が分かったか", "", overview, "", "## 確認できた事実", ""]
    for fact in facts:
        lines.extend([f"- {fact.statement_ja or fact.statement} [^{fact.fact_id}]", ""])
    lines.extend(
        [
            "## それが意味すること",
            "",
            implications.strip()
            + "".join(f" [^{fact_id}]" for fact_id in implication_fact_ids or []),
            "",
            "## まだ分からないこと",
            "",
            uncertainties.strip(),
            "",
            "## 出典",
            "",
        ]
    )
    for fact in facts:
        lines.extend(
            [
                f"[^{fact.fact_id}]: [{fact.source_title}]({fact.source_url})",
                f"  - 根拠引用: 「{normalize_evidence(fact.evidence_quote)}」",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def write_grounded_page(
    client: Any, title: str, facts: list[AtomicFact], feedback: str = ""
) -> str:
    material = [
        {
            "fact_id": fact.fact_id,
            "source_language_statement": fact.statement,
            "japanese_display_statement": fact.statement_ja,
            "source_title": fact.source_title,
        }
        for fact in facts
    ]
    response = client.chat(
        "Create concise Japanese framing for a Japanese Wiki page. Return JSON only. Translate "
        "requested_title into a natural Japanese title within 40 characters; do not echo an English "
        "title. Preserve product names and acronyms, but express the relation in Japanese. overview "
        "must be 1-3 informative sentences that "
        "synthesize only the supplied Japanese display statements; cite each factual sentence with "
        "the supplied fact_id using [^fact-id]. Do not add facts, numbers, dates, entities or "
        "capabilities. implications must be explicitly labeled as interpretation, use only "
        "conservative conclusions supported by the verified statements, and avoid unproved benefits "
        "such as efficiency or cost savings. Select the relevant implication_fact_ids to cite that "
        "interpretation. uncertainties must state only what the "
        "facts do not establish. Do not include Markdown headings or URLs.",
        json.dumps(
            {"requested_title": title, "verified_facts": material, "feedback": feedback},
            ensure_ascii=False,
        ),
        GROUNDED_PAGE_SCHEMA,
    )
    return render_grounded_page(
        str(response.get("title", "")).strip(),
        facts,
        str(response.get("implications", "")).strip(),
        str(response.get("uncertainties", "")).strip(),
        str(response.get("overview", "")).strip(),
        [
            str(fact_id)
            for fact_id in response.get("implication_fact_ids", [])
            if str(fact_id) in {fact.fact_id for fact in facts}
        ],
    )


def validate_grounded_page(page: str, facts: list[AtomicFact]) -> None:
    issues: list[str] = []
    title_match = re.search(r"^#\s+(.+)$", page, re.MULTILINE)
    if not title_match or not re.search(r"[ぁ-んァ-ヶ一-龯]", title_match.group(1)):
        issues.append("日本語のH1タイトルがありません")
    positions: list[int] = []
    for section in GROUNDED_SECTIONS:
        match = re.search(rf"^##\s+{re.escape(section)}\s*$", page, re.MULTILINE)
        if match is None:
            issues.append(f"必須セクション `## {section}` がありません")
        else:
            positions.append(match.start())
    if len(positions) == len(GROUNDED_SECTIONS) and positions != sorted(positions):
        issues.append("必須セクションの順序が違います")
    overview_match = re.search(
        r"^## 何が分かったか\s*$(.*?)(?=^## )", page, re.MULTILINE | re.DOTALL
    )
    known_fact_ids = {fact.fact_id for fact in facts}
    if overview_match:
        overview_ids = set(re.findall(r"\[\^(fact-[^\]]+)\]", overview_match.group(1)))
        if not re.search(r"[\u3040-\u30ff\u3400-\u9fff]", overview_match.group(1)):
            issues.append("概要に日本語の説明がありません")
        invented_overview_ids = overview_ids - known_fact_ids
        if invented_overview_ids:
            issues.append(
                "概要に存在しない事実IDへの脚注があります: "
                + ",".join(sorted(invented_overview_ids))
            )
        elif not overview_ids:
            issues.append(
                "概要に検証済み事実への脚注がありません: " + ",".join(sorted(known_fact_ids))
            )
    implications_match = re.search(
        r"^## それが意味すること\s*$(.*?)(?=^## )", page, re.MULTILINE | re.DOTALL
    )
    if implications_match:
        implication_ids = set(re.findall(r"\[\^(fact-[^\]]+)\]", implications_match.group(1)))
        if not implication_ids or implication_ids - known_fact_ids:
            issues.append("意味づけに検証済み事実への脚注がありません")
    for fact in facts:
        display_statement = fact.statement_ja or fact.statement
        if not re.search(r"[\u3040-\u30ff\u3400-\u9fff]", display_statement):
            issues.append(f"事実 `{fact.fact_id}` の日本語表示文がありません")
        if page.count(f"[^{fact.fact_id}]") < 2:
            issues.append(f"事実 `{fact.fact_id}` の本文参照または脚注がありません")
        if normalize_evidence(fact.evidence_quote) not in normalize_evidence(page):
            issues.append(f"事実 `{fact.fact_id}` の根拠引用がありません")
        if fact.source_url not in page:
            issues.append(f"事実 `{fact.fact_id}` の出典URLがありません")
    allowed_urls = {fact.source_url for fact in facts}
    page_urls = set(re.findall(r"https?://[^\s<>()\]]+", page))
    if page_urls - allowed_urls:
        issues.append("検証済み事実にないURLがあります")
    if issues:
        raise ValueError("; ".join(issues))


def ensure_fact_tables(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS atomic_facts (
            fact_id TEXT PRIMARY KEY,
            statement TEXT NOT NULL,
            statement_ja TEXT NOT NULL DEFAULT '',
            evidence_quote TEXT NOT NULL,
            source_url TEXT NOT NULL,
            source_title TEXT NOT NULL,
            confidence REAL NOT NULL,
            verification_status TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS page_fact_claims (
            page_path TEXT NOT NULL,
            fact_id TEXT NOT NULL,
            PRIMARY KEY (page_path, fact_id),
            FOREIGN KEY (fact_id) REFERENCES atomic_facts(fact_id)
        );
        """
    )
    columns = {
        str(row[1]) for row in connection.execute("PRAGMA table_info(atomic_facts)").fetchall()
    }
    if "statement_ja" not in columns:
        connection.execute(
            "ALTER TABLE atomic_facts ADD COLUMN statement_ja TEXT NOT NULL DEFAULT ''"
        )


def store_page_facts(
    connection: sqlite3.Connection, page_path: str, facts: list[AtomicFact], created_at: str
) -> None:
    ensure_fact_tables(connection)
    for fact in facts:
        connection.execute(
            "INSERT OR REPLACE INTO atomic_facts "
            "(fact_id, statement, statement_ja, evidence_quote, source_url, source_title, "
            "confidence, verification_status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                fact.fact_id,
                fact.statement,
                fact.statement_ja,
                fact.evidence_quote,
                fact.source_url,
                fact.source_title,
                fact.confidence,
                "verified",
                created_at,
            ),
        )
        connection.execute(
            "INSERT OR REPLACE INTO page_fact_claims VALUES (?, ?)",
            (page_path, fact.fact_id),
        )
    connection.commit()
