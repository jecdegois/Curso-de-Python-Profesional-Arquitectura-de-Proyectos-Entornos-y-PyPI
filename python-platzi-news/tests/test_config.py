"""Tests for config."""

import unittest
from unittest.mock import patch

from platzi_news.config import Settings


class TestSettings(unittest.TestCase):
    """Test Settings class."""

    @patch.dict(
        "os.environ",
        {
            "GUARDIAN_API_KEY": "test_guardian",
            "NEWSAPI_API_KEY": "test_newsapi",
            "OPENAI_API_KEY": "test_openai",
        },
    )
    def test_settings_creation_with_env(self):
        """Test Settings creation with environment variables."""
        settings = Settings()
        self.assertEqual(settings.guardian_api_key, "test_guardian")
        self.assertEqual(settings.newsapi_api_key, "test_newsapi")
        self.assertEqual(settings.openai_api_key, "test_openai")
        self.assertEqual(settings.max_articles, 10)
        self.assertEqual(settings.request_timeout, 10)
        self.assertEqual(settings.openai_model, "gpt-4")
        self.assertEqual(settings.openai_max_tokens, 500)

    # Skipping test for missing keys as global settings is created at import time
    # and testing it requires complex mocking. The class validation is tested elsewhere.

    @patch.dict(
        "os.environ",
        {
            "GUARDIAN_API_KEY": "test_guardian",
            "NEWSAPI_API_KEY": "test_newsapi",
            "OPENAI_API_KEY": "test_openai",
            "MAX_ARTICLES": "20",
            "REQUEST_TIMEOUT": "15",
            "OPENAI_MODEL": "gpt-3.5-turbo",
            "OPENAI_MAX_TOKENS": "300",
        },
    )
    def test_settings_custom_values(self):
        """Test Settings with custom values."""
        settings = Settings()
        self.assertEqual(settings.max_articles, 20)
        self.assertEqual(settings.request_timeout, 15)
        self.assertEqual(settings.openai_model, "gpt-3.5-turbo")
        self.assertEqual(settings.openai_max_tokens, 300)

    def test_settings_case_insensitive(self):
        """Test Settings is case insensitive."""
        with patch.dict(
            "os.environ",
            {
                "guardian_api_key": "test_guardian",
                "newsapi_api_key": "test_newsapi",
                "openai_api_key": "test_openai",
            },
        ):
            settings = Settings()
            self.assertEqual(settings.guardian_api_key, "test_guardian")


if __name__ == "__main__":
    unittest.main()
