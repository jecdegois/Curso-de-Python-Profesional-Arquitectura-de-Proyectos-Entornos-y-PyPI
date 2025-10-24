"""The Guardian news source."""

import logging

import httpx
import requests

from ..config import settings
from ..core.exceptions import APIError
from ..core.models import Article
from . import NewsSource

logger = logging.getLogger(__name__)


class GuardianAPI(NewsSource):
    """News source for The Guardian API."""

    BASE_URL = "https://content.guardianapis.com/search"

    def __init__(self) -> None:
        self.api_key = settings.guardian_api_key

    def fetch_articles(self, query: str) -> list[Article]:
        """Fetch articles from The Guardian."""

        logger.debug(f"Fetching articles from The Guardian for query: {query}")

        params: dict[str, str | int] = {
            "q": query,
            "api-key": self.api_key,
            "show-fields": "headline,trailText,shortUrl",
            "page-size": settings.max_articles,
        }
        try:
            logger.debug("Making request to The Guardian API")
            response = requests.get(
                self.BASE_URL, params=params, timeout=settings.request_timeout
            )
            response.raise_for_status()
            data = response.json()
            articles = []
            for result in data.get("response", {}).get("results", []):
                fields = result.get("fields", {})
                articles.append(
                    Article(
                        title=result.get("webTitle", ""),
                        description=fields.get("trailText", ""),
                        url=result.get("webUrl", ""),
                    )
                )
            logger.info(f"Retrieved {len(articles)} articles from The Guardian")
            return articles
        except requests.RequestException as e:
            logger.error(f"Failed to fetch articles from The Guardian: {e}")
            msg = (
                f"Error al obtener artículos de The Guardian: {e}. "
                "Verifique su conexión a internet y la clave de API de The Guardian."
            )
            raise APIError(msg) from e

    async def afetch_articles(self, query: str) -> list[Article]:
        logger.debug(f"Fetching articles from The Guardian for query: {query}")

        params: dict[str, str | int] = {
            "q": query,
            "api-key": self.api_key,
            "show-fields": "headline,trailText,shortUrl",
            "page-size": settings.max_articles,
        }
        logger.debug("Making request to The Guardian API")
        async with httpx.AsyncClient() as client:
            response = await client.get(
                self.BASE_URL, params=params, timeout=settings.request_timeout
            )
            data = response.json()
            articles = []
            for result in data.get("response", {}).get("results", []):
                fields = result.get("fields", {})
                articles.append(
                    Article(
                        title=result.get("webTitle", ""),
                        description=fields.get("trailText", ""),
                        url=result.get("webUrl", ""),
                    )
                )
            logger.info(f"Retrieved {len(articles)} articles from The Guardian")
            return articles
