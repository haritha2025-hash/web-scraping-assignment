import re
from urllib.parse import urljoin


def clean_text(value):
    """Clean extra spaces and convert empty values to an empty string."""

    if value is None:
        return ""

    value = str(value).strip()
    value = re.sub(r"\s+", " ", value)

    return value


def strip_quotes(value):
    """Remove surrounding quotation marks from text."""

    value = clean_text(value)

    if len(value) >= 2:
        if (value.startswith('"') and value.endswith('"')) or (
            value.startswith("'") and value.endswith("'")
        ):
            value = value[1:-1].strip()

    return value


def clean_price(value):
    """Convert a price such as £51.77 into a numeric value."""

    value = clean_text(value)

    if not value:
        return ""

    value = re.sub(r"[^\d.]", "", value)

    if not value:
        return ""

    try:
        return float(value)
    except ValueError:
        return ""


def clean_rating(value):
    """Convert a rating word such as Three into an integer."""

    rating_map = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
    }

    value = clean_text(value).lower()

    if value in rating_map:
        return rating_map[value]

    try:
        number = int(value)

        if 1 <= number <= 5:
            return number

    except ValueError:
        pass

    return ""


def clean_tags(value):
    """Clean and standardize comma-separated tags."""

    value = clean_text(value)

    if not value:
        return ""

    tags = [
        clean_text(tag)
        for tag in value.split(",")
        if clean_text(tag)
    ]

    return ", ".join(tags)


def normalize_url(value, base_url=""):
    """Convert a URL into an absolute URL."""

    value = clean_text(value)

    if not value:
        return ""

    return urljoin(base_url, value)


def clean_record(record):
    """Clean all fields in one scraped record."""

    cleaned = dict(record)

    cleaned["source"] = clean_text(cleaned.get("source"))
    cleaned["source_url"] = normalize_url(
        cleaned.get("source_url", "")
    )
    cleaned["name_or_title"] = strip_quotes(
        cleaned.get("name_or_title", "")
    )
    cleaned["category"] = clean_text(
        cleaned.get("category")
    )
    cleaned["price"] = clean_price(
        cleaned.get("price")
    )
    cleaned["rating"] = clean_rating(
        cleaned.get("rating")
    )
    cleaned["author"] = clean_text(
        cleaned.get("author")
    )
    cleaned["tags"] = clean_tags(
        cleaned.get("tags")
    )
    cleaned["description"] = clean_text(
        cleaned.get("description")
    )
    cleaned["scraped_at"] = clean_text(
        cleaned.get("scraped_at")
    )

    return cleaned