# Multi-Source Web Scraping & Data Consolidation

## 1. Project Overview

This project is a Python-based web scraping and data-processing pipeline that collects data from two public practice websites:

- Books to Scrape
- Quotes to Scrape

The pipeline performs the following steps:

1. Scraping
2. Cleaning
3. Validation
4. Deduplication
5. Consolidation
6. CSV and JSON output
7. Logging

The complete workflow can be executed with one command:

```bash
python main.py

2. Data Sources
Books to Scrape
URL:
https://books.toscrape.com/
The scraper collects:
- Book title
- Price
- Rating
- Source
- Source URL
The scraper follows the Next pagination link until there are no more pages.
Quotes to Scrape
URL:
https://quotes.toscrape.com/
The scraper collects:
- Quote text
- Author
- Tags
- Source
- Source URL
The scraper also follows the Next pagination link until there are no more pages.
Both websites are public practice websites and no authentication, CAPTCHA bypass, or access-control bypass is used.
3. Technologies Used
- Python 3.10.10
- Requests
- BeautifulSoup4
- lxml
- pytest
- CSV
- JSON
- Python logging
4. Project Structure
WEB_SCRAPING_ASSIGNMENT
│
├── logs
│   └── scraper.log
│
├── output
│   ├── final_dataset.csv
│   └── summary_report.json
│
├── processing
│   ├── cleaning.py
│   ├── validation.py
│   └── deduplication.py
│
├── scrapers
│   ├── base_scraper.py
│   ├── books_scraper.py
│   └── quotes_scraper.py
│
├── tests
│   └── test_processing.py
│
├── main.py
├── requirements.txt
├── README.md
└── AI_USAGE.md

5. Installation
Make sure Python 3.10 or a compatible Python version is installed.
Install the required dependencies:
python -m pip install -r requirements.txt

6. Running the Project
From the project root directory, run:
python main.py

The program runs the complete scraping and processing pipeline.
7. Scraping Process
The program uses separate scraper classes for each website.
Books Scraper
books_scraper.py extracts book records and follows the website's next-page link.
Quotes Scraper
quotes_scraper.py extracts quote records and follows the website's next-page link.
Pagination is dynamic and is not based on a hard-coded number of pages.
The common HTTP functionality is handled by:
scrapers/base_scraper.py

The HTTP helper includes:
- Requests session
- User-Agent
- Timeout
- Retry handling
- Request delay
- UTF-8 response handling
- Error logging
8. Common Data Model
All records are converted to the following common schema:
source
source_url
name_or_title
category
price
rating
author
tags
description
scraped_at

Fields that do not apply to a particular source are left empty.
No unavailable data is invented.
9. Data Cleaning
Cleaning is implemented in:
processing/cleaning.py

The cleaning process includes:
- Removing unnecessary whitespace
- Removing surrounding quotation marks
- Converting prices into numeric values
- Converting rating words into numbers
- Cleaning comma-separated tags
- Normalizing URLs
- Cleaning individual records
For example:
"  Hello    World  "

becomes:
Hello World

A rating such as:
Three

is converted to:
3

10. Data Validation
Validation is implemented in:
processing/validation.py

Each record is checked for:
- Allowed source
- Non-empty name or title
- Valid HTTP/HTTPS source URL
- Numeric non-negative price when present
- Rating between 1 and 5 when present
Invalid records are rejected and the rejection reason is recorded in the summary report.
11. Deduplication
Deduplication is implemented in:
processing/deduplication.py

Text is normalized before creating a duplicate fingerprint.
Normalization includes:
- Converting text to lowercase
- Removing punctuation
- Collapsing extra spaces
Books
The fingerprint uses:
source + title

Quotes
The fingerprint uses:
source + author + first 50 characters of quote

Duplicate records are removed from the final dataset.
12. Error Handling
The program handles request failures without crashing the complete workflow.
Each source is processed independently.
If one scraper encounters a failure, the other source is still attempted.
Errors are written to:
logs/scraper.log

Warnings are also logged when records are rejected during validation.
13. Output Files
The program generates:
Final Dataset
output/final_dataset.csv

This contains the cleaned, validated and deduplicated records from both sources.
Summary Report
output/summary_report.json

The summary contains:
- Raw record counts
- Cleaned record counts
- Rejected record counts
- Rejection reasons
- Duplicate count
- Final record count
- Execution start time
- Execution end time
- Duration
- Reconciliation check
Log File
logs/scraper.log

This contains execution information, warnings and errors.
14. Test Results
Automated tests are included in:
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
Test command:
python -m pytest -q

Test result from the development run:
8 passed in 0.04s

15. Sample Execution Results
During the development run on 2026-10-06:
Books records: 1000
Quotes records: 100
Raw records: 1100
Valid cleaned records: 1100
Duplicates removed: 1
Final records: 1099
Rejected records: 0

The program completed successfully and generated the required CSV, JSON and log files.
16. Reconciliation
The summary report verifies:
Raw records - Rejected records - Duplicate records = Final records

For the development run:
1100 - 0 - 1 = 1099

Therefore:
Reconciliation: PASS

17. Assumptions and Limitations
The common schema contains fields that are not applicable to every source.
For example:
- Books do not currently populate author, tags, or description.
- Quotes do not have a price or rating.
- Book category and description are left empty because this implementation does not make separate book detail-page requests.
- The quote source URL represents the page from which the quote was scraped.
Only data available from the implemented selectors is included.
18. Testing the Project from a Clean Environment
To reproduce the project:
1. Create a Python 3.10 or compatible environment.
2. Install dependencies:
python -m pip install -r requirements.txt

3. Run the scraper:
python main.py

4. Run the tests:
python -m pytest -q

5. Check:
output/final_dataset.csv
output/summary_report.json
logs/scraper.log

19. AI Usage
AI assistance was used during development for:
- Understanding the assignment requirements
- Structuring the Python project
- Developing scraper components
- Developing cleaning, validation and deduplication functions
- Developing automated tests
- Reviewing implementation issues
Detailed AI usage, prompts, changes and verification are documented separately in:
AI_USAGE.md

The final implementation was tested by running the scraper and automated tests.
