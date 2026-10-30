import re
import sqlite3
from pathlib import Path
from typing import Any

from src.atomic_facts import (
    AtomicFact,
    evidence_material,
    fact_validation_issues,
    filter_reviewed_facts,
    localize_verified_facts,
    extract_verified_facts,
    render_grounded_page,
    store_page_facts,
    unsupported_critical_tokens,
    validate_fact,
    validate_grounded_page,
)
from src.wiki_agent import SearchResult


def _fact(fact_id: str = "fact-1") -> AtomicFact:
    return AtomicFact(
        fact_id=fact_id,
        statement="HPAは2から6 Podへスケールするよう設定された。",
        evidence_quote="HPA was configured to scale from 2 to 6 pods.",
        source_url="https://example.com/hpa",
        source_title="HPA test",
        confidence=0.95,
    )


def test_validate_fact_requires_allowed_url_and_verbatim_quote() -> None:
    material = "URL: https://example.com/hpa\nHPA was configured to scale from 2 to 6 pods."
    allowed = {"https://example.com/hpa"}

    assert validate_fact(_fact(), material, allowed) is True
    assert validate_fact(_fact(), "different text", allowed) is False
    assert (
        validate_fact(
            AtomicFact("x", "claim", "different text", "https://invalid.test", "x", 1.0),
            material,
            allowed,
        )
        is False
    )


def test_validate_fact_requires_quote_to_belong_to_the_cited_source() -> None:
    fact = _fact()
    materials = {
        "https://example.com/hpa": "A different source excerpt.",
        "https://example.com/other": "HPA was configured to scale from 2 to 6 pods.",
    }

    assert validate_fact(fact, materials, set(materials)) is False


def test_validate_fact_rejects_quote_that_only_matches_after_whitespace_normalization() -> None:
    fact = AtomicFact(
        "fact-space",
        "The target is 6 replicas.",
        "The target is 6 replicas.",
        "https://example.com/hpa",
        "HPA test",
        0.95,
    )

    assert fact_validation_issues(
        fact,
        {fact.source_url: "The target is  6 replicas."},
        {fact.source_url},
    ) == ["quote_not_found_in_cited_source"]


def test_extract_verified_facts_maps_normalized_quote_to_exact_source_span() -> None:
    examples = [
        ("The target is  6 replicas.", "The target is 6 replicas.", "The target is 6 replicas."),
        (
            "The target is <strong>6</strong> replicas.",
            "The target is 6 replicas.",
            "The target is 6 replicas.",
        ),
        ("The service uses A &amp; B.", "The service uses A & B.", "The service uses A and B."),
    ]

    for source_text, model_quote, statement in examples:

        class Extractor:
            def chat(
                self, system: str, prompt: str, response_schema: dict[str, Any]
            ) -> dict[str, Any]:
                return {
                    "facts": [
                        {
                            "statement": statement,
                            "evidence_quote": model_quote,
                            "source_id": "source-1",
                            "confidence": 0.9,
                        }
                    ]
                }

        facts, rejected = extract_verified_facts(
            Extractor(),
            "Test",
            "",
            [SearchResult("Source", "https://example.com/source", source_text)],
        )

        assert rejected == {}
        assert len(facts) == 1
        assert facts[0].evidence_quote == source_text


def test_extract_verified_facts_maps_source_id_to_canonical_url() -> None:
    class Extractor:
        def __init__(self) -> None:
            self.prompt = ""

        def chat(self, system: str, prompt: str, response_schema: dict[str, Any]) -> dict[str, Any]:
            self.prompt = prompt
            return {
                "facts": [
                    {
                        "statement": "A cache avoids repeated database queries.",
                        "evidence_quote": "A cache avoids repeated database queries.",
                        "source_id": "source-2",
                        "confidence": 0.9,
                    }
                ]
            }

    extractor = Extractor()
    facts, rejected = extract_verified_facts(
        extractor,
        "Cache behavior",
        "",
        [
            SearchResult("First", "https://example.com/first", "Unrelated text."),
            SearchResult(
                "Canonical source title",
                "https://example.com/canonical?ref=exact",
                "A cache avoids repeated database queries.",
            ),
        ],
    )

    assert "SOURCE ID: source-2" in extractor.prompt
    assert facts[0].source_url == "https://example.com/canonical?ref=exact"
    assert facts[0].source_title == "Canonical source title"
    assert rejected == {}


def test_extract_verified_facts_keeps_every_source_when_snippets_are_large() -> None:
    class Extractor:
        def __init__(self) -> None:
            self.prompt = ""

        def chat(self, system: str, prompt: str, response_schema: dict[str, Any]) -> dict[str, Any]:
            self.prompt = prompt
            return {"facts": []}

    extractor = Extractor()
    # Five sources near the real max_pages_fetched/snippet-length config (5 sources,
    # up to 12000 chars each) should all reach the model instead of being silently
    # dropped by a fixed character-count cutoff.
    sources = [
        SearchResult(f"Source {i}", f"https://example.com/source-{i}", "x" * 12000)
        for i in range(1, 6)
    ]

    extract_verified_facts(extractor, "Topic", "", sources)

    for i in range(1, 6):
        assert f"SOURCE ID: source-{i}" in extractor.prompt


def test_extract_verified_facts_rejects_unknown_source_id_even_with_a_url() -> None:
    class Extractor:
        def chat(self, system: str, prompt: str, response_schema: dict[str, Any]) -> dict[str, Any]:
            return {
                "facts": [
                    {
                        "statement": "A cache avoids repeated database queries.",
                        "evidence_quote": "A cache avoids repeated database queries.",
                        "source_id": "source-999",
                        "source_url": "https://example.com/source",
                        "confidence": 0.9,
                    }
                ]
            }

    facts, rejected = extract_verified_facts(
        Extractor(),
        "Cache behavior",
        "",
        [
            SearchResult(
                "Source", "https://example.com/source", "A cache avoids repeated database queries."
            )
        ],
    )

    assert facts == []
    assert rejected == {"candidate-1": "source_id_not_allowed"}


def test_extraction_deduplicates_identical_candidates() -> None:
    class Extractor:
        def chat(self, *args: Any) -> dict[str, Any]:
            item = {
                "statement": "A cache saves work.",
                "evidence_quote": "A cache saves work.",
                "source_id": "source-1",
                "confidence": 0.9,
            }
            return {"facts": [item, dict(item)]}

    facts, rejected = extract_verified_facts(
        Extractor(),
        "Cache",
        "",
        [SearchResult("Source", "https://example.com", "A cache saves work.")],
    )
    assert len(facts) == 1
    assert rejected == {"candidate-2": "duplicate_fact"}


def test_validate_fact_allows_source_language_claim_text() -> None:
    fact = AtomicFact(
        "fact-en",
        "The Horizontal Pod Autoscaler scales applications based on CPU utilization targets.",
        "The Horizontal Pod Autoscaler scales your application based on CPU utilization.",
        "https://example.com/hpa",
        "HPA test",
        0.95,
    )

    assert (
        fact_validation_issues(fact, {fact.source_url: fact.evidence_quote}, {fact.source_url})
        == []
    )


def test_unsupported_critical_tokens_rejects_number_missing_from_quote() -> None:
    assert unsupported_critical_tokens(
        "アラートは最大6 Podに達した時に発火した。",
        "At peak load, the alert fired.",
    ) == {"6", "pod"}


def test_filter_reviewed_facts_fails_closed_for_omitted_ids() -> None:
    facts = [_fact("fact-1"), _fact("fact-2")]

    accepted, rejected = filter_reviewed_facts(
        facts,
        {"accepted_fact_ids": ["fact-1"], "rejected": []},
    )

    assert [fact.fact_id for fact in accepted] == ["fact-1"]
    assert rejected == {"fact-2": "reviewer_omitted_fact"}


def test_render_grounded_page_has_small_readable_structure_and_fact_links() -> None:
    page = render_grounded_page(
        "EKSのHPA負荷試験",
        [_fact()],
        implications="これは検証済み事実から分けた解釈です。",
        uncertainties="他の構成で同じ結果になるかは未確認です。",
    )

    assert [line for line in page.splitlines() if line.startswith("## ")] == [
        "## 何が分かったか",
        "## 確認できた事実",
        "## それが意味すること",
        "## まだ分からないこと",
        "## 出典",
    ]
    assert "[^fact-1]" in page
    assert "根拠引用" in page


def test_evidence_material_includes_urls_and_snippets() -> None:
    sources = [SearchResult("HPA test", "https://example.com/hpa", "scale from 2 to 6")]

    material = evidence_material("research", sources)

    assert "research" in material
    assert "https://example.com/hpa" in material
    assert "scale from 2 to 6" in material


def test_validate_grounded_page_accepts_a_single_well_supported_source() -> None:
    fact = _fact()
    page = render_grounded_page(
        "EKSのHPA負荷試験",
        [fact, _fact("fact-2")],
        implications="検証された範囲では、負荷に応じた増減を確認できます。",
        uncertainties="別構成での再現性は未確認です。",
        overview="HPAは2から6 Podへスケールする設定です。[^fact-1]",
        implication_fact_ids=["fact-1"],
    )

    validate_grounded_page(page, [fact, _fact("fact-2")])


def test_validate_grounded_page_rejects_missing_fact_citation() -> None:
    fact = _fact()
    page = render_grounded_page(
        "EKSのHPA負荷試験",
        [fact],
        implications="解釈です。",
        uncertainties="未確認です。",
        overview="HPAは2から6 Podへスケールする設定です。[^fact-1]",
        implication_fact_ids=["fact-1"],
    ).replace("[^fact-1]", "", 1)

    try:
        validate_grounded_page(page, [fact])
    except ValueError as error:
        assert "fact-1" in str(error)
    else:
        raise AssertionError("missing fact citation must be rejected")


def test_validate_grounded_page_requires_japanese_display_for_english_fact() -> None:
    fact = AtomicFact(
        "fact-en",
        "The Horizontal Pod Autoscaler scales applications based on CPU utilization.",
        "The Horizontal Pod Autoscaler scales your application based on CPU utilization.",
        "https://example.com/hpa",
        "HPA test",
        0.95,
    )
    page = render_grounded_page(
        "HPAの概要",
        [fact],
        "解釈です。",
        "未確認です。",
        "HPAはCPU利用率を使います。[^fact-en]",
        ["fact-en"],
    )

    try:
        validate_grounded_page(page, [fact])
    except ValueError as error:
        assert "日本語表示文" in str(error)
    else:
        raise AssertionError("an English fact must not appear as the page display text")


class _GroundedWriter:
    def chat(self, system: str, prompt: str, response_schema: dict[str, Any]) -> dict[str, Any]:
        if "facts" in response_schema.get("properties", {}):
            return {
                "facts": [
                    {
                        "statement": "HPAは2から6 Podへスケールするよう設定された。",
                        "evidence_quote": "HPA was configured to scale from 2 to 6 pods.",
                        "source_id": "source-1",
                        "confidence": 0.95,
                    },
                    {
                        "statement": "負荷試験では失敗がなかった。",
                        "evidence_quote": "The load test recorded zero failed requests.",
                        "source_id": "source-1",
                        "confidence": 0.95,
                    },
                ]
            }
        ids = re.findall(r'"fact_id":\s*"([^"]+)"', prompt)
        return {
            "title": "EKSのHPA負荷試験",
            "overview": "HPAの設定ではPod数を調整します。[^%s]" % (ids[0] if ids else "missing"),
            "implication_fact_ids": ids[:1],
            "implications": "以下は検証済み事実に基づく解釈です。",
            "uncertainties": "他の環境での再現性は未確認です。",
        }


class _GroundedReviewer:
    def chat(self, system: str, prompt: str, response_schema: dict[str, Any]) -> dict[str, Any]:
        ids = re.findall(r'"fact_id":\s*"([^"]+)"', prompt)
        return {"accepted_fact_ids": ids, "rejected": []}

    def review(self, content: str, research_context: str = "") -> dict[str, object]:
        return {"approved": True, "issues": []}


class _EnglishFactTranslator:
    def chat(self, system: str, prompt: str, response_schema: dict[str, Any]) -> dict[str, Any]:
        if "translations" in response_schema.get("properties", {}):
            ids = re.findall(r'"fact_id":\s*"([^"]+)"', prompt)
            return {
                "translations": [
                    {"fact_id": fact_id, "statement_ja": "HPAはCPU利用率に基づきPod数を調整する。"}
                    for fact_id in ids
                ]
            }
        raise AssertionError("review is delegated to the reviewer")


def test_localize_verified_facts_keeps_english_claim_and_adds_japanese_display_text() -> None:
    fact = AtomicFact(
        "fact-en",
        "The Horizontal Pod Autoscaler scales applications based on CPU utilization.",
        "The Horizontal Pod Autoscaler scales your application based on CPU utilization.",
        "https://example.com/hpa",
        "HPA test",
        0.95,
    )

    localized, rejected = localize_verified_facts(
        _EnglishFactTranslator(),
        _GroundedReviewer(),
        [fact],
    )

    assert rejected == {}
    assert len(localized) == 1
    assert localized[0].statement == fact.statement
    assert localized[0].statement_ja == "HPAはCPU利用率に基づきPod数を調整する。"


def test_write_grounded_and_review_accepts_two_verified_facts(tmp_path: Path) -> None:
    from src.wiki_agent import write_grounded_and_review

    source = SearchResult(
        "HPA test",
        "https://example.com/hpa",
        "HPA was configured to scale from 2 to 6 pods. The load test recorded zero failed requests.",
    )
    accepted, page, review, facts = write_grounded_and_review(
        _GroundedWriter(),
        _GroundedReviewer(),
        Path("10_Knowledge/HPA.md"),
        [source],
        "",
        tmp_path,
    )

    assert accepted is True
    assert len(facts) == 2
    assert "## 確認できた事実" in page
    assert review == {"approved": True, "issues": []}


def test_write_grounded_and_review_stops_when_verified_facts_are_insufficient(
    tmp_path: Path,
) -> None:
    from src.wiki_agent import write_grounded_and_review

    source = SearchResult("HPA", "https://example.com/hpa", "unrelated")
    accepted, page, review, facts = write_grounded_and_review(
        _GroundedWriter(),
        _GroundedReviewer(),
        Path("10_Knowledge/HPA.md"),
        [source],
        "",
        tmp_path,
    )

    assert accepted is False
    assert page == ""
    assert facts == []
    assert review["result"] == "insufficient_evidence"


def test_store_page_facts_links_verified_facts_to_page(tmp_path: Path) -> None:
    connection = sqlite3.connect(tmp_path / "facts.sqlite3")
    fact = AtomicFact(
        "fact-1",
        "HPA was configured to scale from 2 to 6 pods.",
        "HPA was configured to scale from 2 to 6 pods.",
        "https://example.com/hpa",
        "HPA test",
        0.95,
        "HPAは2から6 Podへ拡張する設定だった。",
    )

    store_page_facts(connection, "10_Knowledge/HPA.md", [fact], "2026-10-23T00:00:00Z")

    assert connection.execute(
        "SELECT statement, statement_ja, verification_status FROM atomic_facts "
        "WHERE fact_id = 'fact-1'"
    ).fetchone() == (
        "HPA was configured to scale from 2 to 6 pods.",
        "HPAは2から6 Podへ拡張する設定だった。",
        "verified",
    )
    assert connection.execute("SELECT page_path, fact_id FROM page_fact_claims").fetchall() == [
        ("10_Knowledge/HPA.md", "fact-1")
    ]
