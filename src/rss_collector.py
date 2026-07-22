"""RSS collection for the news-driven (経路A) Wiki growth path.

Minimally ported from AIBackgroundWorker's ``packages/info_collector``: only the
RSS fetching needed to seed the existing web-search + Writer pipeline. The
summarizer, search planner, and news/search collectors are intentionally left
behind -- the produced Wiki page itself is the "report".

関連モジュール:
- src/wiki_agent.py - StateDB.ingest_rss_candidates / plan_rss_action で利用
"""

from __future__ import annotations

import calendar
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

import feedparser  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class RSSEntry:
    """One article discovered via an RSS/Atom feed."""

    title: str
    url: str
    snippet: str = ""
    published_at: datetime | None = None
    source_name: str = ""


class RSSCollector:
    """Fetch entries from RSS/Atom feeds using feedparser."""

    def collect(self, feed_url: str, max_entries: int = 10) -> list[RSSEntry]:
        """Return up to ``max_entries`` entries from a single feed.

        Network or parse errors never raise: they are logged and yield an empty
        list so one broken feed cannot stall the whole run.
        """
        feed_url = feed_url.strip()
        if not feed_url:
            return []
        try:
            feed = feedparser.parse(feed_url)
        except Exception as error:  # noqa: BLE001 - a bad feed must not crash the run
            logger.warning("RSS取得エラー feed_url=%s: %s", feed_url, error)
            return []

        feed_title = feed.feed.get("title", "Unknown Feed")
        entries: list[RSSEntry] = []
        for entry in feed.entries[:max_entries]:
            url = str(entry.get("link", "")).strip()
            title = str(entry.get("title", "")).strip()
            if not url or not title:
                continue
            published_at = None
            parsed = entry.get("published_parsed") or entry.get("updated_parsed")
            if parsed:
                published_at = datetime.fromtimestamp(calendar.timegm(parsed), tz=timezone.utc)
            entries.append(
                RSSEntry(
                    title=title,
                    url=url,
                    snippet=str(entry.get("summary", "")),
                    published_at=published_at,
                    source_name=str(feed_title),
                )
            )
        return entries

    def collect_multiple(
        self, feed_urls: Sequence[str], max_entries_per_feed: int = 10
    ) -> list[RSSEntry]:
        """Collect entries from several feeds in order."""
        all_entries: list[RSSEntry] = []
        for url in feed_urls:
            all_entries.extend(self.collect(url, max_entries_per_feed))
        return all_entries


def load_rss_sources(path: Path) -> list[str]:
    """Read feed URLs from a text file, skipping blank lines and ``#`` comments."""
    if not path.exists():
        return []
    sources: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            sources.append(line)
    return sources
