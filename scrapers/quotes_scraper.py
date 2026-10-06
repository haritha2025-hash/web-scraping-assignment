from scrapers.base_scraper import BaseScraper


class QuotesScraper(BaseScraper):
    """Scraper for Quotes to Scrape."""

    START_URL = "https://quotes.toscrape.com/"

    def scrape(self):
        """Scrape quotes from all available pages."""

        records = []
        current_url = self.START_URL

        while current_url:
            soup = self.fetch_page(current_url)

            if soup is None:
                break

            quotes = soup.select("div.quote")

            for quote in quotes:
                text_element = quote.select_one("span.text")
                author_element = quote.select_one("small.author")

                text = ""
                if text_element:
                    text = text_element.get_text(strip=True)

                author = ""
                if author_element:
                    author = author_element.get_text(strip=True)

                tag_elements = quote.select("a.tag")
                tags = ", ".join(
                    tag.get_text(strip=True)
                    for tag in tag_elements
                )

                record = {
                    "source": "quotes",
                    "source_url": current_url,
                    "name_or_title": text,
                    "category": "",
                    "price": "",
                    "rating": "",
                    "author": author,
                    "tags": tags,
                    "description": "",
                    "scraped_at": "",
                }

                records.append(record)

            current_url = self.get_next_page(soup, current_url)

        return records