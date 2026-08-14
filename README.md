# Product Parsers

This repository contains one Django project backed by PostgreSQL and three independent product parsers:

- Requests with BeautifulSoup
- Selenium
- Playwright

Each parser collects the required product data, prints one structured dictionary, and stores a separately identifiable record in the shared `Product` model.

## Requirements

- Python 3.10 or newer
- PostgreSQL
- Google Chrome or Chromium
- PGAdmin for the required CSV export

## Installation

Run the following commands from the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m playwright install chromium
Copy-Item .env.example .env
```

Edit `.env` and replace the example secret key and PostgreSQL password before running Django or any parser.

## PostgreSQL Setup

Open `psql` as a PostgreSQL administrator and run:

```sql
CREATE USER braincomua_user WITH PASSWORD 'replace-with-a-local-password';
CREATE DATABASE braincomua_db OWNER braincomua_user;
```

Set the same database name, user, password, host, and port in `.env`.

## Django Setup

After the Django project files are present, run:

```powershell
python manage.py migrate
python manage.py check
```

## Django Integration Checks

After the integration scripts are present, run:

```powershell
python modules\check_db_write.py
python modules\check_db_read.py
```

## Parser Commands

Run each parser independently:

```powershell
python modules\1_requests_bs4.py
python modules\2_selenium.py
python modules\3_playwright.py
```

Keep `BROWSER_HEADLESS=False` while selectors and browser actions are being verified. Change it only after both browser workflows work visibly.

## Parser Configuration

Target URLs and search queries can be adjusted in `.env`:

```env
REQUESTS_PRODUCT_URL=https://brain.com.ua/ukr/Mobilniy_telefon_Apple_iPhone_16_Pro_Max_256GB_Black_Titanium-p1145443.html
BROWSER_SEARCH_QUERY=Apple iPhone 15 128GB Black
BROWSER_HEADLESS=False
BROWSER_TIMEOUT_SECONDS=30
```

## Results

Export PostgreSQL data to CSV through PGAdmin and store the CSV files and PostgreSQL dump in `results`. Do not create a Python CSV export script.
