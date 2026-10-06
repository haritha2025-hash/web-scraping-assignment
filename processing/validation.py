from urllib.parse import urlparse


ALLOWED_SOURCES = {"books", "quotes"}


def validate_record(record):
    """
    Validate one cleaned record.

    Returns:
        (True, None) when valid
        (False, reason) when invalid
    """

    source = record.get("source", "")
    name = record.get("name_or_title", "")
    source_url = record.get("source_url", "")
    price = record.get("price", "")
    rating = record.get("rating", "")

    # Check source.
    if source not in ALLOWED_SOURCES:
        return False, "invalid_source"

    # Check title / quote text.
    if not name or not str(name).strip():
        return False, "missing_name_or_title"

    # Check URL.
    if not source_url:
        return False, "missing_source_url"

    parsed_url = urlparse(source_url)

    if parsed_url.scheme not in {"http", "https"}:
        return False, "invalid_source_url"

    # Check price when present.
    if price != "":
        try:
            numeric_price = float(price)

            if numeric_price < 0:
                return False, "negative_price"

        except (TypeError, ValueError):
            return False, "invalid_price"

    # Check rating when present.
    if rating != "":
        try:
            numeric_rating = int(rating)

            if numeric_rating < 1 or numeric_rating > 5:
                return False, "invalid_rating"

        except (TypeError, ValueError):
            return False, "invalid_rating"

    return True, None