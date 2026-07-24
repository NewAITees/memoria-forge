"""Research utilities ported from AIBackgroundWorker."""

from src.research.ddg_client import DDGSearchClient, filter_search_results
from src.research.page_fetcher import fetch_pages

__all__ = ["DDGSearchClient", "filter_search_results", "fetch_pages"]
