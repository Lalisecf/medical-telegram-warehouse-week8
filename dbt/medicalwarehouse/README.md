# Medical Telegram Data Warehouse

## Project Overview

This project is part of the **10 Academy KAIM Week 8 Interim Challenge**.

The objective is to build an end-to-end data pipeline that extracts data from Ethiopian public medical Telegram channels, stores the raw data in PostgreSQL, and transforms it into a dimensional warehouse using dbt.

The warehouse supports downstream analytics and machine learning applications.

---

# Project Architecture

```
Telegram Channels
        │
        ▼
Telegram Scraper (Telethon)
        │
        ▼
JSON Files + Images
        │
        ▼
PostgreSQL (Raw Layer)
        │
        ▼
dbt Staging Models
        │
        ▼
Star Schema
        │
        ▼
Analytics
```

---

# Technologies Used

* Python 3.11
* Telethon
* PostgreSQL
* dbt (dbt-postgres)
* psycopg2
* python-dotenv
* Git & GitHub

---

# Project Structure

```
medical-telegram-warehouse-week8/

├── .github/
├── api/
├── data/
│   └── raw/
│       ├── images/
│       └── telegram_messages/
├── dbt/
│   └── medicalwarehouse/
├── logs/
├── notebooks/
├── scripts/
│   └── load_raw.py
├── src/
│   └── scraper.py
├── tests/
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
├── README.md
└── .env
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/Lalisecf/medical-telegram-warehouse-week8.git
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file.

```
API_ID=xxxxxxxx
API_HASH=xxxxxxxx
PHONE=+251xxxxxxxxx

DB_HOST=localhost
DB_PORT=5432
DB_NAME=medicalwarehouse
DB_USER=postgres
DB_PASSWORD=mypassword
```

---

# Task 1 — Telegram Scraper

Run

```bash
python src/scraper.py
```

The scraper

* Connects to Telegram
* Reads multiple channels
* Downloads images
* Saves JSON files
* Creates logs

Output

```
data/raw/telegram_messages/YYYY-MM-DD/

CheMed123.json
Lobelia4Cosmetics.json
tikvahpharma.json
```

Images are stored under

```
data/raw/images/{channel}
```

---

# Task 2 — PostgreSQL Loading

Run

```bash
python scripts/load_raw.py
```

The script

* Creates schema `raw`
* Creates table `raw.telegram_messages`
* Reads all JSON files
* Inserts records into PostgreSQL
* Prevents duplicate inserts

---

# dbt

Run models

```bash
dbt run
```

Run tests

```bash
dbt test
```

Generate documentation

```bash
dbt docs generate
```

Serve documentation

```bash
dbt docs serve
```

---

# Star Schema

The warehouse consists of

* dim_channels
* dim_dates
* fct_messages

These models are built from the staging model.

---

# Data Quality

Built-in dbt tests

* unique
* not_null
* relationships

Custom tests

* assert_no_future_messages
* assert_positive_views

---

# Results

Successfully completed

* Telegram scraping
* Image downloading
* JSON generation
* PostgreSQL loading
* dbt staging
* Star schema
* Documentation generation
* Data quality testing

---

# Author

Lalise Fufi

10 Academy KAIM Week 8 Challenge
