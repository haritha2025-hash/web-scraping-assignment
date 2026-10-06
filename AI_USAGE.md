# AI Usage Documentation

## 1. Overview

AI assistance was used during the development of this project.

The AI was used as a development support tool for understanding the assignment, planning the project structure, writing implementation components, creating tests, and troubleshooting issues.

The final implementation was reviewed, executed, and tested in the local development environment.

---

## 2. AI Tool Used

Tool:

- ChatGPT

The AI was used for coding assistance, explanation of implementation decisions, project organization, and troubleshooting.

---

## 3. Purpose of AI Assistance

AI assistance was used for the following purposes:

1. Understanding the assignment requirements.
2. Planning the project folder structure.
3. Creating the common scraper functionality.
4. Developing the Books to Scrape scraper.
5. Developing the Quotes to Scrape scraper.
6. Developing data-cleaning functions.
7. Developing validation functions.
8. Developing duplicate detection and removal.
9. Connecting all components through `main.py`.
10. Creating automated tests.
11. Troubleshooting test execution issues.
12. Preparing project documentation.

---

## 4. Example Prompts Used

Examples of prompts used during development include:

### Project Structure

"Help me create a Python project structure for a multi-source web scraping assignment with separate scraper, processing, testing, output, and logging folders."

### HTTP Scraper

"Create a reusable Python HTTP helper using requests, timeout, retry handling, User-Agent, UTF-8 encoding, and a small delay between requests."

### Books Scraper

"Create a Python scraper for Books to Scrape that follows the next-page link dynamically and extracts the title, price, rating, and source URL."

### Quotes Scraper

"Create a Python scraper for Quotes to Scrape that follows pagination and extracts quote text, author, tags, and source URL."

### Cleaning

"Create Python cleaning functions for text, prices, ratings, tags, and URLs according to the assignment requirements."

### Validation

"Create validation functions that check allowed sources, required names, valid URLs, non-negative prices, and ratings from 1 to 5."

### Deduplication

"Create duplicate detection using normalized text and fingerprints for books and quotes."

### Testing

"Create pytest tests for cleaning, validation, and duplicate detection."

### Troubleshooting

"Help me troubleshoot a ModuleNotFoundError when running pytest in VS Code."

---

## 5. Parts Assisted by AI

AI assistance was used while developing:

- `scrapers/base_scraper.py`
- `scrapers/books_scraper.py`
- `scrapers/quotes_scraper.py`
- `processing/cleaning.py`
- `processing/validation.py`
- `processing/deduplication.py`
- `main.py`
- `tests/test_processing.py`
- `README.md`

AI assistance was also used to explain the purpose of the different components and how they connect together.

---

## 6. Human Review and Changes

The generated implementation was reviewed during development.

The project was executed locally using:

```text
python main.py

The scraper successfully collected:
- 1000 book records
- 100 quote records
The resulting raw record count was:
1100

The processing pipeline produced:
1100 valid cleaned records
1 duplicate removed
1099 final records
0 rejected records

The output files were generated successfully:
output/final_dataset.csv
output/summary_report.json
logs/scraper.log

7. Testing and Verification
Automated tests were created in:
tests/test_processing.py

The tests cover:
- Text cleaning
- Price cleaning
- Rating cleaning
- Tag cleaning
- Valid record validation
- Invalid rating validation
- Duplicate fingerprint detection
- Duplicate removal
The tests were executed using:
python -m pytest -q

The result was:
8 passed in 0.04s

The complete scraping pipeline was also executed using:
python main.py

and completed successfully.
8. Troubleshooting
During testing, running:
pytest -q

resulted in a module import error:
ModuleNotFoundError: No module named 'processing'

The issue was resolved by running pytest through the same Python environment:
python -m pytest -q

After this change, all 8 tests passed.
9. Incorrect or Adjusted Suggestions
During development, the initial pytest command:
pytest -q

did not correctly resolve the project modules in the current VS Code environment.
The command was changed to:
python -m pytest -q

This successfully executed the tests.
The implementation was verified by running the scraper and tests locally.
10. Verification Responsibility
AI assistance does not replace testing or verification.
The final implementation was verified by:
1. Running the complete scraper.
2. Checking the number of records collected from both sources.
3. Checking that the output files were created.
4. Running automated tests.
5. Checking the reconciliation calculation.
6. Reviewing the generated project structure and outputs.
11. Final Verification Results
Final development run:
Books records: 1000
Quotes records: 100
Raw records: 1100
Rejected records: 0
Duplicates removed: 1
Final records: 1099

Reconciliation:
1100 - 0 - 1 = 1099

Test result:
8 passed in 0.04s

The project completed successfully and produced the required output files.