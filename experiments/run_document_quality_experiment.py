"""Generate one real page without touching the live Vault and record every attempt."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.wiki_agent import (  # noqa: E402
    Config,
    create_client,
    create_reviewer_client,
    format_deep_research,
    normalize_page,
    review_is_blocking,
    validate_page_content,
)
from src.research.deep_research import research_article  # noqa: E402


OUTPUT = ROOT / "experiments" / "document_quality_result"
THEME = "Cerebras CS-4の推論性能、GPU比較、導入上の制約"
REASON = (
    "Cerebras CS-4について、最大30倍という性能主張の比較条件、公式仕様、"
    "第三者情報、価格・消費電力・適用モデルの制約を区別して検証する。"
)


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    config = Config.load(ROOT / "config.json")
    writer = create_client(config)
    reviewer = create_reviewer_client(config)
    research_path = OUTPUT / "research.json"
    if research_path.exists():
        deep = json.loads(research_path.read_text(encoding="utf-8"))
    else:
        deep = research_article(
            writer,
            title=THEME,
            snippet=REASON,
            max_queries=min(config.max_searches, 3),
            max_pages=config.max_pages_fetched,
            research_reason=REASON,
        )
    context, sources = format_deep_research(deep)
    research_path.write_text(
        json.dumps(deep, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    feedback = ""
    attempts: list[dict[str, object]] = []
    verdict: dict[str, object] = {"accepted": False, "attempts": attempts}
    for attempt in range(1, 3):
        page = normalize_page(
            Path("10_Knowledge/Cerebras CS-4.md"),
            writer.write(
                THEME,
                REASON,
                sources,
                feedback=feedback,
                research_context=context,
            ),
            sources,
        )
        (OUTPUT / f"attempt-{attempt}.md").write_text(page, encoding="utf-8")
        try:
            validate_page_content(page, sources)
        except ValueError as error:
            feedback = str(error)
            attempts.append(
                {"attempt": attempt, "deterministic": "failed", "error": feedback}
            )
            continue
        review = reviewer.review(page, context)
        attempts.append(
            {"attempt": attempt, "deterministic": "passed", "review": review}
        )
        if not review_is_blocking(review):
            verdict["accepted"] = True
            verdict["accepted_attempt"] = attempt
            break
        feedback = json.dumps(review.get("issues", []), ensure_ascii=False)

    verdict["source_count"] = len(sources)
    verdict["research_query_count"] = len(deep.get("queries", []))
    (OUTPUT / "verdict.json").write_text(
        json.dumps(verdict, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(verdict, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
