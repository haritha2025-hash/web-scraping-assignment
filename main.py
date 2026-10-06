import csv
import json
import logging
import time
from datetime import datetime
from pathlib import Path

from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper
from processing.cleaning import clean_record
from processing.validation import validate_record
from processing.deduplication import remove_duplicates


# ---------------------------------------------------------
# PROJECT PATHS
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

CSV_FILE = OUTPUT_DIR / "final_dataset.csv"
SUMMARY_FILE = OUTPUT_DIR / "summary_report.json"
LOG_FILE = LOG_DIR / "scraper.log"


# ---------------------------------------------------------
# CSV COLUMNS
# ---------------------------------------------------------

FIELDNAMES = [
    "source",
    "source_url",
    "name_or_title",
    "category",
    "price",
    "rating",
    "author",
    "tags",
    "description",
    "scraped_at",
]


# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------

def setup_logging():
    """Create console and file logging."""

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Remove existing handlers so logging isn't duplicated.
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(
        LOG_FILE,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# ---------------------------------------------------------
# CSV OUTPUT
# ---------------------------------------------------------

def write_csv(records):
    """Write final records to CSV."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(
        CSV_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES
        )

        writer.writeheader()

        for record in records:
            writer.writerow(record)


# ---------------------------------------------------------
# SOURCE COUNTS
# ---------------------------------------------------------

def count_by_source(records):
    """Count records belonging to each source."""

    counts = {
        "books": 0,
        "quotes": 0,
    }

    for record in records:
        source = record.get("source")

        if source in counts:
            counts[source] += 1

    return counts


# ---------------------------------------------------------
# MAIN SCRAPING PROCESS
# ---------------------------------------------------------

def main():

    setup_logging()

    start_time = datetime.now()

    logging.info("Scraping job started.")

    raw_records = []
    rejected_records = []
    rejected_reasons = {}

    # -----------------------------------------------------
    # BOOKS
    # -----------------------------------------------------

    logging.info("Starting Books to Scrape.")

    try:
        books_scraper = BooksScraper()
        books_records = books_scraper.scrape()

        logging.info(
            "Books scraping completed: %d records.",
            len(books_records)
        )

        raw_records.extend(books_records)

    except Exception as error:
        logging.error(
            "Books scraper failed: %s",
            error
        )

    # -----------------------------------------------------
    # QUOTES
    # -----------------------------------------------------

    logging.info("Starting Quotes to Scrape.")

    try:
        quotes_scraper = QuotesScraper()
        quotes_records = quotes_scraper.scrape()

        logging.info(
            "Quotes scraping completed: %d records.",
            len(quotes_records)
        )

        raw_records.extend(quotes_records)

    except Exception as error:
        logging.error(
            "Quotes scraper failed: %s",
            error
        )

    # -----------------------------------------------------
    # RAW COUNTS
    # -----------------------------------------------------

    raw_counts = count_by_source(raw_records)

    logging.info(
        "Total raw records collected: %d",
        len(raw_records)
    )

    # -----------------------------------------------------
    # CLEANING + VALIDATION
    # -----------------------------------------------------

    cleaned_records = []

    for record in raw_records:

        try:
            cleaned = clean_record(record)

            is_valid, reason = validate_record(cleaned)

            if is_valid:
                cleaned_records.append(cleaned)

            else:
                rejected_records.append(cleaned)

                rejected_reasons[reason] = (
                    rejected_reasons.get(reason, 0) + 1
                )

                logging.warning(
                    "Rejected record: %s",
                    reason
                )

        except Exception as error:

            rejected_records.append(record)

            reason = "processing_error"

            rejected_reasons[reason] = (
                rejected_reasons.get(reason, 0) + 1
            )

            logging.warning(
                "Record processing failed: %s",
                error
            )

    cleaned_counts = count_by_source(cleaned_records)

    logging.info(
        "Valid cleaned records: %d",
        len(cleaned_records)
    )

    # -----------------------------------------------------
    # DEDUPLICATION
    # -----------------------------------------------------

    unique_records, duplicate_records = remove_duplicates(
        cleaned_records
    )

    logging.info(
        "Duplicates removed: %d",
        len(duplicate_records)
    )

    # -----------------------------------------------------
    # ADD SCRAPED TIME
    # -----------------------------------------------------

    scraped_at = datetime.now().isoformat(
        timespec="seconds"
    )

    for record in unique_records:
        record["scraped_at"] = scraped_at

    # -----------------------------------------------------
    # WRITE CSV
    # -----------------------------------------------------

    write_csv(unique_records)

    logging.info(
        "Final dataset written to: %s",
        CSV_FILE
    )

    # -----------------------------------------------------
    # EXECUTION INFORMATION
    # -----------------------------------------------------

    end_time = datetime.now()

    duration_seconds = (
        end_time - start_time
    ).total_seconds()

    # -----------------------------------------------------
    # SUMMARY REPORT
    # -----------------------------------------------------

    final_counts = count_by_source(unique_records)

    summary = {
        "execution": {
            "start_time": start_time.isoformat(
                timespec="seconds"
            ),
            "end_time": end_time.isoformat(
                timespec="seconds"
            ),
            "duration_seconds": duration_seconds,
        },

        "raw_records": {
            "books": raw_counts["books"],
            "quotes": raw_counts["quotes"],
            "total": len(raw_records),
        },

        "cleaned_records": {
            "books": cleaned_counts["books"],
            "quotes": cleaned_counts["quotes"],
            "total": len(cleaned_records),
        },

        "rejected_records": {
            "total": len(rejected_records),
            "reasons": rejected_reasons,
        },

        "duplicates": {
            "total": len(duplicate_records),
        },

        "final_records": {
            "books": final_counts["books"],
            "quotes": final_counts["quotes"],
            "total": len(unique_records),
        },

        "reconciliation": {
            "raw_minus_rejected_minus_duplicates": (
                len(raw_records)
                - len(rejected_records)
                - len(duplicate_records)
            ),
            "final_count": len(unique_records),
            "counts_match": (
                len(raw_records)
                - len(rejected_records)
                - len(duplicate_records)
                == len(unique_records)
            ),
        },
    }

    with open(
        SUMMARY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            summary,
            file,
            indent=4
        )

    logging.info(
        "Summary report written to: %s",
        SUMMARY_FILE
    )

    logging.info(
        "Scraping job completed successfully."
    )


# ---------------------------------------------------------
# PROGRAM ENTRY POINT
# ---------------------------------------------------------

if __name__ == "__main__":
    main()