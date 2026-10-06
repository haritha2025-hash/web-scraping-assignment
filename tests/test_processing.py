from processing.cleaning import (
    clean_text,
    clean_price,
    clean_rating,
    clean_tags,
)

from processing.validation import validate_record

from processing.deduplication import (
    create_fingerprint,
    remove_duplicates,
)


def test_clean_text():
    assert clean_text("  Hello    World  ") == "Hello World"


def test_clean_price():
    assert clean_price("£51.77") == 51.77


def test_clean_rating():
    assert clean_rating("Three") == 3


def test_clean_tags():
    assert clean_tags("life, love,   books") == "life, love, books"


def test_valid_record():
    record = {
        "source": "books",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Test Book",
        "category": "",
        "price": 10.50,
        "rating": 4,
        "author": "",
        "tags": "",
        "description": "",
        "scraped_at": "",
    }

    valid, reason = validate_record(record)

    assert valid is True
    assert reason is None


def test_invalid_rating():
    record = {
        "source": "books",
        "source_url": "https://books.toscrape.com/",
        "name_or_title": "Test Book",
        "category": "",
        "price": 10.50,
        "rating": 6,
        "author": "",
        "tags": "",
        "description": "",
        "scraped_at": "",
    }

    valid, reason = validate_record(record)

    assert valid is False
    assert reason == "invalid_rating"


def test_duplicate_detection():
    record1 = {
        "source": "books",
        "name_or_title": "The Great Book",
    }

    record2 = {
        "source": "books",
        "name_or_title": " the great book! ",
    }

    assert create_fingerprint(record1) == create_fingerprint(record2)


def test_remove_duplicates():
    records = [
        {
            "source": "books",
            "name_or_title": "The Great Book",
        },
        {
            "source": "books",
            "name_or_title": " the great book! ",
        },
    ]

    unique_records, duplicate_records = remove_duplicates(records)

    assert len(unique_records) == 1
    assert len(duplicate_records) == 1