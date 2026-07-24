"""DDG検索結果URLからプレインテキストを抽出するフェッチャー."""

from __future__ import annotations

import logging
from typing import Dict, List

import requests  # type: ignore[import-untyped]
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

_HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
_REMOVE_TAGS = {"script", "style", "nav", "footer", "header", "aside", "form", "noscript"}


def _extract_text(html: str, per_page_limit: int) -> str:
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.find_all(_REMOVE_TAGS):
        tag.decompose()

    # article > main > body の優先順で本文エリアを探す
    container = soup.find("article") or soup.find("main") or soup.find("body")
    if container is None:
        return ""

    paragraphs = container.find_all("p")
    if not paragraphs:
        text = container.get_text(separator="\n", strip=True)
        return text[:per_page_limit]

    lines: List[str] = []
    total = 0
    for p in paragraphs:
        line = p.get_text(separator=" ", strip=True)
        if not line:
            continue
        if total + len(line) > per_page_limit:
            remaining = per_page_limit - total
            if remaining > 0:
                lines.append(line[:remaining])
            break
        lines.append(line)
        total += len(line)

    return "\n".join(lines)


def fetch_pages(
    results: List[Dict[str, str]],
    total_limit: int = 12000,
    per_page_limit: int = 3000,
    timeout: int = 8,
) -> List[Dict[str, str]]:
    """検索結果リストの各URLを順位順にfetchしてpage_contentを付与して返す。

    累計文字数がtotal_limitに達した時点で以降のURLはスキップする。
    fetchに失敗したエントリはpage_content=""のまま返す。

    Args:
        results: DDGSearchClientが返す結果リスト
        total_limit: 全ページ合計の文字数上限
        per_page_limit: 1ページあたりの文字数上限
        timeout: HTTP接続タイムアウト（秒）

    Returns:
        page_contentフィールドを追加した結果リスト
    """
    enriched: List[Dict[str, str]] = []
    total_chars = 0

    for result in results:
        entry = dict(result)
        url = entry.get("url", "")

        if not url or total_chars >= total_limit:
            entry["page_content"] = ""
            enriched.append(entry)
            continue

        try:
            resp = requests.get(url, headers=_HEADERS, timeout=timeout)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding

            remaining_budget = total_limit - total_chars
            effective_limit = min(per_page_limit, remaining_budget)
            text = _extract_text(resp.text, effective_limit)

            entry["page_content"] = text
            total_chars += len(text)
            logger.debug("Fetched %d chars from %s (total=%d)", len(text), url, total_chars)
        except Exception as exc:  # noqa: BLE001
            logger.warning("page_fetcher: skipped %s — %s", url, exc)
            entry["page_content"] = ""

        enriched.append(entry)

    return enriched

