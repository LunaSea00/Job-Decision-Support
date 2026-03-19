#!/usr/bin/env python3
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.db import Base, SessionLocal, engine
from app.models.company import Company
from app.models.search_index import SearchIndex
from app.models.signal import Signal
from app.utils.normalizer import normalize_company_name
from app.utils.url_helpers import extract_domain


def main() -> None:
    data_path = PROJECT_ROOT / "data" / "sample_companies.json"
    rows = json.loads(data_path.read_text(encoding="utf-8"))

    Base.metadata.create_all(bind=engine)

    session = SessionLocal()
    try:
        for row in rows:
            normalized_name = normalize_company_name(row["legal_name"])
            company = Company(
                corporate_id=row["corporate_id"],
                legal_name=row["legal_name"],
                normalized_name=normalized_name,
                address=row.get("address"),
                prefecture=row.get("prefecture"),
                website=row.get("website"),
                industry=row.get("industry"),
                is_listed=row.get("is_listed"),
            )
            session.merge(company)

            aliases = [normalize_company_name(alias) for alias in row.get("aliases", [])]
            search_index = SearchIndex(
                corporate_id=row["corporate_id"],
                legal_name=row["legal_name"],
                normalized_name=normalized_name,
                aliases=",".join(aliases) if aliases else None,
                website_domain=extract_domain(row.get("website")),
                prefecture=row.get("prefecture"),
            )
            existing_index = (
                session.query(SearchIndex)
                .filter(SearchIndex.corporate_id == row["corporate_id"])
                .one_or_none()
            )
            if existing_index:
                existing_index.legal_name = search_index.legal_name
                existing_index.normalized_name = search_index.normalized_name
                existing_index.aliases = search_index.aliases
                existing_index.website_domain = search_index.website_domain
                existing_index.prefecture = search_index.prefecture
            else:
                session.add(search_index)

            existing_signal = session.get(Signal, row["corporate_id"])
            if existing_signal is None:
                session.add(Signal(corporate_id=row["corporate_id"]))

        session.commit()
        print(f"Seeded {len(rows)} companies")
    finally:
        session.close()


if __name__ == "__main__":
    main()
