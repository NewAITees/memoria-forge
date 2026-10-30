from pathlib import Path

from experiments.atomic_fact_graph import (
    Fact,
    FactStore,
    SourceDocument,
    candidate_relation_pairs,
    normalize_evidence,
    unsupported_critical_tokens,
    validate_fact,
)


def test_validate_fact_accepts_exact_evidence_after_whitespace_normalization() -> None:
    source = SourceDocument("doc-1", "Title", "https://example.com", "A fact\n with spacing.")
    fact = Fact("fact-1", "A fact with spacing.", "fact with spacing.", "doc-1", 0.9)

    assert normalize_evidence(source.content) == "A fact with spacing."
    assert validate_fact(fact, source) is True


def test_validate_fact_rejects_evidence_not_present_in_source() -> None:
    source = SourceDocument("doc-1", "Title", "https://example.com", "Only supported text.")
    fact = Fact("fact-1", "Invented claim", "not in the source", "doc-1", 0.9)

    assert validate_fact(fact, source) is False


def test_fact_store_keeps_only_verified_facts_and_relations(tmp_path: Path) -> None:
    database = tmp_path / "facts.sqlite3"
    source = SourceDocument("doc-1", "Title", "https://example.com", "The limit is 40.")
    valid = Fact("fact-1", "The limit is 40.", "The limit is 40.", "doc-1", 0.95)
    invalid = Fact("fact-2", "The limit is 80.", "The limit is 80.", "doc-1", 0.95)

    with FactStore(database) as store:
        store.add_source(source)
        assert store.add_fact(valid) is True
        assert store.add_fact(invalid) is False
        store.add_relation("fact-1", "fact-1", "same", 1.0)

        assert store.fact_count() == 1
        assert store.relation_count() == 1
        assert store.active_facts()[0].statement == "The limit is 40."


def test_unsupported_critical_tokens_detects_number_word_missing_from_quote() -> None:
    statement = "The alert fired at the configured maximum of six pods."
    quote = "At peak load, the alert fired and a notification was emitted."

    assert unsupported_critical_tokens(statement, quote) == {"six"}


def test_unsupported_critical_tokens_accepts_supported_numbers_and_acronyms() -> None:
    statement = "HPA scaled from 2 to 6 pods at 55% CPU."
    quote = "Kubernetes HPA scaled from 2 to 6 pods at a target of 55% average CPU utilization."

    assert unsupported_critical_tokens(statement, quote) == set()


def test_candidate_relation_pairs_excludes_same_document_and_unrelated_facts() -> None:
    facts = [
        Fact("a", "Alex works at Google as an engineer.", "q", "doc-1", 1.0),
        Fact("b", "Alex works at Stripe as a PM.", "q", "doc-2", 1.0),
        Fact("c", "GPU utilization reached 90 percent.", "q", "doc-3", 1.0),
        Fact("d", "Alex moved to Seattle.", "q", "doc-1", 1.0),
    ]

    assert candidate_relation_pairs(facts) == [(facts[0], facts[1])]
