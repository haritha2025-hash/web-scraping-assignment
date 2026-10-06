import hashlib
import re


def normalize_for_fingerprint(value):
    """Normalize a value before creating a duplicate fingerprint."""

    value = "" if value is None else str(value).lower()

    # Remove punctuation.
    value = re.sub(r"[^\w\s]", "", value)

    # Collapse multiple spaces.
    value = re.sub(r"\s+", " ", value).strip()

    return value


def create_fingerprint(record):
    """
    Create a fingerprint for identifying duplicate records.

    Books:
        source + title

    Quotes:
        source + author + first 50 characters of quote
    """

    source = normalize_for_fingerprint(
        record.get("source", "")
    )

    name = normalize_for_fingerprint(
        record.get("name_or_title", "")
    )

    if source == "books":
        fingerprint_text = f"{source}|{name}"

    elif source == "quotes":
        author = normalize_for_fingerprint(
            record.get("author", "")
        )

        quote_start = name[:50]

        fingerprint_text = (
            f"{source}|{author}|{quote_start}"
        )

    else:
        fingerprint_text = (
            f"{source}|{name}"
        )

    return hashlib.sha256(
        fingerprint_text.encode("utf-8")
    ).hexdigest()


def remove_duplicates(records):
    """
    Remove duplicate records.

    Returns:
        unique_records,
        duplicate_records
    """

    seen = set()
    unique_records = []
    duplicate_records = []

    for record in records:
        fingerprint = create_fingerprint(record)

        if fingerprint in seen:
            duplicate_records.append(record)
        else:
            seen.add(fingerprint)
            unique_records.append(record)

    return unique_records, duplicate_records