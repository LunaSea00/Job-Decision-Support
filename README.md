# Company Info MVP

Minimal FastAPI backend for Japanese company information aggregation.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/seed_sample_data.py
uvicorn app.main:app --reload
```

## Endpoints

- `GET /health`
- `GET /search?q=ABC`
- `GET /company/{corporate_id}`
- `POST /company/{corporate_id}/refresh-signals`
