"""Tests for analyzer."""

import unittest
from unittest.mock import Mock, patch

from platzi_news.analysis.analyzer import OpenAIAnalyzer, get_analyzer
from platzi_news.core.exceptions import AnalysisError
from platzi_news.core.models import Article


class TestOpenAIAnalyzer(unittest.TestCase):
    """Test OpenAIAnalyzer."""

    @patch("platzi_news.analysis.analyzer.OpenAI")
    def test_analyze_success(self, mock_openai):
        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "Test answer"
        mock_client.chat.completions.create.return_value = mock_response

        analyzer = OpenAIAnalyzer("fake_key")
        articles = [Article("Test", "Desc", "http://example.com")]
        answer = analyzer.analyze(articles, "What is this about?")
        self.assertEqual(answer, "Test answer")

    @patch("platzi_news.analysis.analyzer.OpenAI")
    def test_analyze_no_articles(self, mock_openai):
        analyzer = OpenAIAnalyzer("fake_key")
        answer = analyzer.analyze([], "Question")
        self.assertEqual(answer, "No se encontraron artículos para analizar.")

    @patch("platzi_news.analysis.analyzer.OpenAI")
    def test_analyze_error(self, mock_openai):
        mock_client = Mock()
        mock_openai.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API error")

        analyzer = OpenAIAnalyzer("fake_key")
        articles = [Article("Test", "Desc", "http://example.com")]
        with self.assertRaises(AnalysisError):
            analyzer.analyze(articles, "Question")


class TestGetAnalyzer(unittest.TestCase):
    """Test get_analyzer factory."""

    @patch("platzi_news.config.settings")
    def test_get_analyzer_success(self, mock_settings):
        mock_settings.openai_api_key = "fake_key"
        analyzer = get_analyzer()
        self.assertIsInstance(analyzer, OpenAIAnalyzer)


if __name__ == "__main__":
    unittest.main()
