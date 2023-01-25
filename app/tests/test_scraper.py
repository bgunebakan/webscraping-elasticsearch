import unittest
from unittest.mock import patch
import requests
from scrapers.scraper import get_article


class TestGetArticle(unittest.TestCase):

    url = "https://en.wikipedia.org/wiki/Special:Random"
    html_content = b'<html><body><h1>Test Title</h1><div class="reflist">Test Article</div><ol class="references">Test Reference</ol><li id="footer-info-lastmod">2022-01-01</li></body></html>'

    @patch("requests.get")
    def test_get_article_success(self, mock_get):
        """Test the get_article function with a successful response"""

        # Set up the mock response
        mock_response = requests.Response()
        mock_response.url = self.url
        mock_response.status_code = 200
        mock_response._content = self.html_content
        mock_get.return_value = mock_response

        result = get_article(self.url)

        # Assert the results
        self.assertEqual(
            result,
            {
                "article_url": "https://en.wikipedia.org/wiki/Special:Random",
                "title": "Test Title",
                "article": "Test Article",
                "reference": "Test Reference",
                "last_modified": "2022-01-01",
            },
        )

    @patch("requests.get")
    def test_get_article_failure(self, mock_get):
        """Test the get_article function with a failed response"""
        # Set up the mock response
        mock_response = requests.Response()
        mock_response.url = self.url
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        # Test the function
        result = get_article(self.url)

        # Assert the results
        self.assertEqual(result, None)

    @patch("requests.get")
    def test_get_article_attribute_error(self, mock_get):
        """Test the get_article function with an AttributeError"""
        # Set up the mock response
        mock_response = requests.Response()
        mock_response.url = self.url
        mock_response.status_code = 200
        mock_response._content = b'<html><body><h1>Test Title</h1><div class="reflist">Test Article</div></body></html>'
        mock_get.return_value = mock_response

        # Test the function
        result = get_article(self.url)

        # Assert the results
        self.assertEqual(result, None)
