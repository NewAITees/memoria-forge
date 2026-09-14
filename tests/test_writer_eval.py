from experiments.writer_eval import count_truncations, summarize


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


def test_count_truncations_ignores_old_and_unrelated_lines() -> None:
    log = "\n".join(
        [
            'time=2026-09-14T23:59:59+09:00 level=WARN msg="truncating input prompt"',
            'time=2026-09-15T00:00:00+09:00 level=WARN msg="truncating input prompt"',
            'time=2026-09-15T00:01:00+09:00 level=INFO msg="request complete"',
            'time=2026-09-15T00:02:00+09:00 level=WARN msg="truncating input prompt"',
        ]
    )

    assert count_truncations(log, "2026-09-15T00:00:00+09:00") == 2
