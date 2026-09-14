from experiments.writer_eval import summarize


def test_summarize_counts_passes_and_rejection_reasons() -> None:
    results = [
        {"target": "a", "accepted": True, "reason": ""},
        {"target": "b", "accepted": False, "reason": "必須セクション `## 結論` がありません; 日本語のH1タイトルがありません"},
        {"target": "c", "accepted": False, "reason": "日本語のH1タイトルがありません"},
    ]
    summary = summarize(results)
    assert summary["total"] == 3
    assert summary["passed"] == 1
    assert summary["reasons"] == {
        "日本語のH1タイトルがありません": 2,
        "必須セクション `## 結論` がありません": 1,
    }


def test_summarize_handles_no_results() -> None:
    assert summarize([]) == {"total": 0, "passed": 0, "reasons": {}}
