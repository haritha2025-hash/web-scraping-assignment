from urllib.parse import urljoin

from scrapers.base_scraper import BaseScraper


class BooksScraper(BaseScraper):
    """Scraper for Books to Scrape."""

    START_URL = "https://books.toscrape.com/"

    def scrape(self):
        """Scrape books from all available pages."""

        records = []
        current_url = self.START_URL

        while current_url:
            soup = self.fetch_page(current_url)

            if soup is None:
                break

            books = soup.select("article.product_pod")

            for book in books:
                title_element = book.select_one("h3 > a")
                price_element = book.select_one("p.price_color")
                rating_element = book.select_one("p.star-rating")

                title = ""
                if title_element:
                    title = title_element.get("title", "").strip()

                price = ""
                if price_element:
                    price = price_element.get_text(strip=True)

                rating = ""
                if rating_element:
                    rating_classes = rating_element.get("class", [])
                    rating_words = [
                        word for word in rating_classes
                        if word != "star-rating"
                    ]

                    if rating_words:
                        rating = rating_words[0]

                book_url = ""
                if title_element and title_element.get("href"):
                    book_url = urljoin(
                        current_url,
                        title_element["href"]
                    )

                record = {
                    "source": "books",
                    "source_url": book_url,
                    "name_or_title": title,
                    "category": "",
                    "price": price,
                    "rating": rating,
                    "author": "",
                    "tags": "",
                    "description": "",
                    "scraped_at": "",
                }

                records.append(record)

            current_url = self.get_next_page(soup, current_url)

        return records