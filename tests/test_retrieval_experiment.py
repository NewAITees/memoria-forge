from pathlib import Path

from experiments.retrieval_experiment import (
    Corpus,
    HybridRetriever,
    KeywordRetriever,
    evaluate,
    run_live_benchmark,
)


def test_retrievers_use_current_vault_shape(tmp_path: Path) -> None:
    (tmp_path / "00_Index").mkdir()
    (tmp_path / "10_Knowledge").mkdir()
    (tmp_path / "00_Index" / "Knowledge MOC.md").write_text("# MOC\n- [[RAG]]", encoding="utf-8")
    (tmp_path / "10_Knowledge" / "RAG.md").write_text("# RAG\nベクトル検索", encoding="utf-8")
    corpus = Corpus(tmp_path)
    questions = [{"query": "RAG ベクトル検索", "relevant": ["10_Knowledge/RAG.md"]}]
    assert evaluate(KeywordRetriever(corpus), questions)["recall_at_k"] == 1.0
    assert evaluate(HybridRetriever(corpus), questions)["recall_at_k"] == 1.0


def test_small_vault_is_reported_as_insufficient(tmp_path: Path) -> None:
    (tmp_path / "Only.md").write_text("# Only\n", encoding="utf-8")
    result = run_live_benchmark(tmp_path, object())
    assert result["status"] == "insufficient_corpus"
