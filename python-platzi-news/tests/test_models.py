"""Tests for models."""

import unittest

from platzi_news.core.models import Article


class TestArticle(unittest.TestCase):
    """Test Article dataclass."""

    def test_article_creation(self):
        """Test creating an Article instance."""
        article = Article(
            title="Test Title", description="Test Description", url="http://example.com"
        )
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.description, "Test Description")
        self.assertEqual(article.url, "http://example.com")

    def test_article_attributes(self):
        """Test Article attributes are accessible."""
        article = Article("Title", "Desc", "URL")
        self.assertTrue(hasattr(article, "title"))
        self.assertTrue(hasattr(article, "description"))
        self.assertTrue(hasattr(article, "url"))

    def test_article_equality(self):
        """Test Article equality."""
        article1 = Article("Title", "Desc", "URL")
        article2 = Article("Title", "Desc", "URL")
        article3 = Article("Different", "Desc", "URL")
        self.assertEqual(article1, article2)
        self.assertNotEqual(article1, article3)


if __name__ == "__main__":
    unittest.main()
