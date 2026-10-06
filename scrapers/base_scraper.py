import logging
import time

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseScraper:
    """Common HTTP and parsing utilities for all scrapers."""

    def __init__(self):
        self.session = requests.Session()

        # Identify our program clearly to the website.
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (compatible; AssignmentScraper/1.0)"
        })

        # Retry temporary HTTP failures.
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

        self.request_delay = 0.5

    def fetch_page(self, url):
        """
        Download a webpage and return a BeautifulSoup object.

        Returns None if the request fails.
        """

        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()

            # Make sure the response is interpreted as UTF-8.
            response.encoding = "utf-8"

            time.sleep(self.request_delay)

            return BeautifulSoup(response.text, "lxml")

        except requests.RequestException as error:
            logging.error("Failed to fetch %s: %s", url, error)
            return None

    @staticmethod
    def get_next_page(soup, current_url):
        """
        Find the next-page link.

        Returns the absolute URL of the next page,
        or None if there is no next page.
        """

        if soup is None:
            return None

        next_link = soup.select_one("li.next > a")

        if next_link and next_link.get("href"):
            from urllib.parse import urljoin

            return urljoin(current_url, next_link["href"])

        return None