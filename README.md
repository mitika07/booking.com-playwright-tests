# Booking.com Test Automation Framework

An AI-assisted Playwright automation framework for Booking.com, built with Python and pytest.

## Tech Stack

- **Python 3.11**
- **Playwright** — browser automation
- **pytest** — test framework
- **pytest-html** — HTML test reports
- **GitHub Actions** — CI/CD pipeline

## Project Structure

```
booking-automation/
├── tests/
│   ├── test_search.py          # Core search functionality
│   ├── test_filters.py         # Filter & sort tests
│   └── test_hotel_details.py   # Hotel details page tests
├── pages/
│   ├── base_page.py            # Shared page methods
│   ├── home_page.py            # Homepage POM
│   ├── search_results_page.py  # Results page POM
│   └── hotel_page.py           # Hotel details POM
├── test_data/
│   └── search_data.json        # Data-driven test inputs
├── .github/workflows/
│   └── test.yml                # CI/CD pipeline
├── conftest.py                 # pytest fixtures
├── pytest.ini                  # pytest config
└── requirements.txt
```

## Setup & Installation

```bash
# Clone the repo
git clone <your-repo-url>
cd booking-automation

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

## Running Tests

```bash
# Run all tests
pytest

# Run a specific test file
pytest tests/test_search.py

# Run with HTML report
pytest --html=reports/report.html --self-contained-html

# Run smoke tests only
pytest -m smoke

# Run in headless mode
pytest --headed=false
```

## CI/CD

Tests run automatically on:
- Every push to `main`
- Every pull request
- Every Monday at 9am (scheduled regression run)

Reports and screenshots are uploaded as GitHub Actions artifacts.

## Design Patterns

- **Page Object Model (POM)** — each page is a separate class
- **Data-driven testing** — test inputs loaded from JSON
- **Fixtures** — shared browser/page setup via `conftest.py`
- **AI-assisted** — test cases and page objects generated and maintained with Claude
