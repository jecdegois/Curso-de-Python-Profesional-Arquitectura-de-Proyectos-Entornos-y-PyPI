"""News sources package."""

from typing import Protocol

from ..core.models import Article


class NewsSource(Protocol):
    """Protocol for news source implementations."""

    def fetch_articles(self, query: str) -> list[Article]:
        """Fetch articles based on the query."""
        ...

    async def afetch_articles(self, query: str) -> list[Article]:
        """Fetch articles based on the query."""
        ...
