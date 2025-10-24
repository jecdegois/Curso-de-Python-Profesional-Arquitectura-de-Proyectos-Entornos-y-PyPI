"""Service layer for news operations."""

from ..analysis.analyzer import OpenAIAnalyzer, get_analyzer
from ..sources import NewsSource
from ..sources.guardian import GuardianAPI
from ..sources.newsapi import NewsAPI
from .models import Article


class NewsService:
    """Service for handling news-related operations.

    This service encapsulates the business logic for searching news articles
    and analyzing them using AI. It acts as an intermediary between the CLI
    and the underlying data sources and analyzers.
    """

    def __init__(self) -> None:
        """Initialize the news service with available sources and analyzer."""
        self.sources: dict[str, NewsSource] = {
            "guardian": GuardianAPI(),
            "newsapi": NewsAPI(),
        }
        self.analyzer: OpenAIAnalyzer = get_analyzer()

    def get_source(self, source_name: str) -> NewsSource:
        """Get a news source by name.

        Args:
            source_name: The name of the news source ('guardian' or 'newsapi').

        Returns:
            The corresponding NewsSource instance.

        Raises:
            ValueError: If the source name is unknown.
        """
        if source_name not in self.sources:
            raise ValueError(f"Unknown source: {source_name}")
        return self.sources[source_name]

    def search_articles(self, source_name: str, query: str) -> list[Article]:
        """Search for articles from a specific source.

        Args:
            source_name: The name of the news source to search in.
            query: The search query string.

        Returns:
            A list of Article objects matching the query.
        """
        source = self.get_source(source_name)
        return source.fetch_articles(query)

    async def asearch_articles(self, source_name: str, query: str) -> list[Article]:
        """Search for articles from a specific source.

        Args:
            source_name: The name of the news source to search in.
            query: The search query string.

        Returns:
            A list of Article objects matching the query.
        """
        source = self.get_source(source_name)
        return await source.afetch_articles(query)

    def analyze_articles(self, articles: list[Article], question: str) -> str:
        """Analyze articles and answer a question.

        Args:
            articles: List of articles to analyze.
            question: The question to answer based on the articles.

        Returns:
            The AI-generated answer.
        """
        return self.analyzer.analyze(articles, question)

    def find_articles_by_keyword(
        self, articles: list[Article], keyword: str
    ) -> list[Article]:
        """Find articles containing a keyword (inefficient implementation)."""
        results = []
        for article in articles:
            if (
                keyword.lower() in article.title.lower()
                or keyword.lower() in article.description.lower()
            ):
                results.append(article)
        return results

    def sort_articles_by_title(self, articles: list[Article]) -> list[Article]:
        """Sort articles by title using bubble sort (O(n²))."""
        n = len(articles)
        for i in range(n):
            for j in range(0, n - i - 1):
                if articles[j].title > articles[j + 1].title:
                    articles[j], articles[j + 1] = articles[j + 1], articles[j]
        return articles

    def count_articles_with_keyword(self, articles: list[Article], keyword: str) -> int:
        """Count articles containing a keyword."""
        count = 0
        for article in articles:
            if (
                keyword.lower() in article.title.lower()
                or keyword.lower() in article.description.lower()
            ):
                count += 1
        return count
