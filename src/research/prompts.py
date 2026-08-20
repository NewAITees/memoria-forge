"""Prompt builders ported verbatim from AIBackgroundWorker.

The prompt text lives in `templates/prompt/*.txt` exactly as it does there, and
these builders assemble the same context blocks. That project produces markedly
more concrete Japanese reports from the same local model, and the earlier attempt
to lift only its *concepts* into this project's own writer shape lost the
quality. So the working units -- query generation, evidence synthesis, and the
theme report -- are carried over intact rather than re-expressed.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

_PROMPT_DIR = Path(__file__).resolve().parents[2] / "templates" / "prompt"


def load_prompt(name: str) -> str:
    """Read `templates/prompt/{name}`."""
    return (_PROMPT_DIR / name).read_text(encoding="utf-8")


def _article_timeline(published_at: str, fetched_at: str, closing_line: str) -> str:
    published = str(published_at or "").strip() or "不明"
    fetched = str(fetched_at or "").strip() or "不明"
    return "\n".join([f"- 公開日時: {published}", f"- 取得日時: {fetched}", closing_line])


def build_search_query_prompt(
    theme: str,
    keywords: list[str],
    category: str,
    summary: str,
    article_published_at: str = "",
    article_fetched_at: str = "",
    importance_reason: str = "",
    relevance_reason: str = "",
) -> dict[str, str]:
    return {
        "system": load_prompt("info_search_query_gen_system.txt"),
        "user": load_prompt("info_search_query_gen_user.txt").format(
            theme=theme,
            keywords=", ".join(keywords),
            category=category,
            summary=summary,
            article_timeline=_article_timeline(
                article_published_at,
                article_fetched_at,
                "- 判別の要点: この時系列を踏まえて、古い情報を最新扱いしない検索クエリを優先すること",
            ),
            importance_reason=importance_reason or "判断理由が記録されていません",
            relevance_reason=relevance_reason or "判断理由が記録されていません",
        ),
    }


def build_result_synthesis_prompt(
    theme: str,
    search_query: str,
    search_results: list[dict[str, str]],
    article_summary: str = "",
    article_published_at: str = "",
    article_fetched_at: str = "",
    importance_score: float = 0.0,
    relevance_score: float = 0.0,
    importance_reason: str = "",
    relevance_reason: str = "",
) -> dict[str, str]:
    results_text = ""
    for index, result in enumerate(search_results[:10], 1):
        results_text += f"\n--- 結果 {index} ---\n"
        results_text += f"タイトル: {result.get('title', 'N/A')}\n"
        results_text += f"要約: {result.get('snippet', 'N/A')}\n"
        results_text += f"URL: {result.get('url', 'N/A')}\n"
        page_content = result.get("page_content", "")
        if page_content:
            results_text += f"本文抜粋:\n{page_content}\n"

    return {
        "system": load_prompt("info_result_synthesis_system.txt"),
        "user": load_prompt("info_result_synthesis_user.txt").format(
            theme=theme,
            article_summary=article_summary or "記事要約が記録されていません",
            article_timeline=_article_timeline(
                article_published_at,
                article_fetched_at,
                "- 要約の書き方: どの時点の情報かが分かるように、本文でも日付・時刻の手がかりを残す",
            ),
            importance_score=importance_score,
            relevance_score=relevance_score,
            importance_reason=importance_reason or "判断理由が記録されていません",
            relevance_reason=relevance_reason or "判断理由が記録されていません",
            search_query=search_query,
            search_results=results_text,
        ),
    }


def build_theme_report_prompt(
    theme: str, articles: list[dict[str, Any]], report_date: str
) -> dict[str, str]:
    """Assemble the per-article detail blocks the theme report is written from."""
    article_details = ""
    for index, article in enumerate(articles, 1):
        article_details += f"\n### 記事 {index}: {article.get('article_title', 'N/A')}\n"
        article_details += f"- **URL**: {article.get('article_url', 'N/A')}\n"
        article_details += f"- **公開日時**: {article.get('article_published_at') or '不明'}\n"
        article_details += f"- **取得日時**: {article.get('article_fetched_at') or '不明'}\n"
        article_details += f"- **重要度**: {float(article.get('importance_score', 0) or 0):.2f}\n"
        importance_reason = article.get("importance_reason", "") or ""
        if importance_reason:
            article_details += f"  - **判断理由**: {importance_reason}\n"
        article_details += f"- **関連度**: {float(article.get('relevance_score', 0) or 0):.2f}\n"
        relevance_reason = article.get("relevance_reason", "") or ""
        if relevance_reason:
            article_details += f"  - **判断理由**: {relevance_reason}\n"
        article_details += f"- **カテゴリ**: {article.get('category', 'N/A')}\n"
        keywords = article.get("keywords", [])
        if isinstance(keywords, str):
            try:
                keywords = json.loads(keywords)
            except ValueError:
                keywords = []
        if keywords:
            article_details += f"- **キーワード**: {', '.join(str(k) for k in keywords[:5])}\n"
        content = article.get("article_content", "") or article.get("snippet", "")
        if content:
            article_details += f"- **概要**: {content[:2000]}{'...' if len(content) > 2000 else ''}\n"
        article_details += f"- **URLからの事実**: {article.get('article_url', 'N/A')}\n"
        article_details += (
            "- **時系列の手がかり**: 記事本文では公開日時・取得日時を踏まえて、"
            "いつ時点の情報かが分かるように記述する\n"
        )

    deep_research_results = ""
    for index, article in enumerate(articles, 1):
        synthesized = article.get("synthesized_content", "")
        if not synthesized:
            continue
        deep_research_results += f"\n### 記事 {index} の深掘り調査結果\n{synthesized}\n"
        sources = article.get("sources", [])
        if isinstance(sources, str):
            try:
                sources = json.loads(sources)
            except ValueError:
                sources = []
        if sources:
            deep_research_results += "\n**参考ソース**:\n"
            for source in sources[:5]:
                url = source.get("url", "") if isinstance(source, dict) else str(source)
                if url:
                    deep_research_results += f"- {url}\n"

    article_timeline = ""
    for index, article in enumerate(articles, 1):
        article_timeline += f"\n- 記事 {index}: "
        article_timeline += f"公開 {article.get('article_published_at') or '不明'} / "
        article_timeline += f"取得 {article.get('article_fetched_at') or '不明'} / "
        article_timeline += "深掘り本文でもこの時系列を手がかりに新旧を判別すること\n"

    return {
        "system": load_prompt("info_theme_report_system.txt"),
        "user": load_prompt("info_theme_report_user.txt").format(
            theme=theme,
            report_date=report_date,
            article_count=len(articles),
            article_details=article_details or "記事詳細なし",
            article_timeline=article_timeline or "時系列メタデータなし",
            deep_research_results=deep_research_results or "深掘り調査結果なし",
        ),
    }
