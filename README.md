# Company Info MVP

Minimal FastAPI backend for Japanese company information aggregation.

## Languages

- English: `README.md`
- 中文: [README.zh-CN.md](README.zh-CN.md)
- 日本語: [README.ja.md](README.ja.md)

## Features

- Search companies with disambiguation fields
- Get company detail by `corporate_id`
- Store structured company and signal data in SQLite
- Refresh website-derived hiring and tech signals

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Pytest

## Project Structure

```text
app/
  api/         HTTP endpoints
  core/        config and database setup
  crawlers/    website signal crawler
  models/      SQLAlchemy models
  schemas/     response schemas
  services/    business logic
  utils/       helpers
data/          sample data and local SQLite DB
scripts/       seed and refresh scripts
tests/         test suite
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/seed_sample_data.py
uvicorn app.main:app --reload
```

## API Endpoints

- `GET /health`
- `GET /search?q=ABC`
- `GET /company/{corporate_id}`
- `POST /company/{corporate_id}/refresh-signals`

## Notes

- `corporate_id` is the only company identity key in this MVP.
- Search results include enough fields to distinguish companies with the same name.
- Signal refresh is currently synchronous.
