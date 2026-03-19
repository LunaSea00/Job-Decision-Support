from app.core.db import Base, SessionLocal, engine
from app.models.company import Company
from app.models.search_index import SearchIndex
from app.models.signal import Signal
from app.services.company_service import get_company_detail
from app.services.search_service import search_companies


def setup_module() -> None:
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        session.query(SearchIndex).delete()
        session.query(Signal).delete()
        session.query(Company).delete()

        company = Company(
            corporate_id="1000000000001",
            legal_name="株式会社ABC",
            normalized_name="ABC",
            address="東京都千代田区1-1-1",
            prefecture="東京都",
            website="https://abc.co.jp",
            industry="IT",
            is_listed=False,
        )
        session.add(company)
        session.add(
            SearchIndex(
                corporate_id="1000000000001",
                legal_name="株式会社ABC",
                normalized_name="ABC",
                aliases="ABC,ABC TOKYO",
                website_domain="abc.co.jp",
                prefecture="東京都",
            )
        )
        session.add(
            Signal(
                corporate_id="1000000000001",
                has_recruit_page=True,
                has_keywords=True,
                recent_update=False,
                has_engineer_keyword=True,
                has_blog=False,
                has_github=True,
            )
        )
        session.commit()
    finally:
        session.close()


def test_search_service_returns_disambiguation_fields() -> None:
    session = SessionLocal()
    try:
        payload = search_companies(session, "ABC")
        assert len(payload) == 1
        assert payload[0].corporate_id == "1000000000001"
        assert payload[0].legal_name == "株式会社ABC"
        assert payload[0].prefecture == "東京都"
        assert payload[0].website == "https://abc.co.jp"
    finally:
        session.close()


def test_company_detail_service_returns_nested_company_and_signals() -> None:
    session = SessionLocal()
    try:
        payload = get_company_detail(session, "1000000000001")
        assert payload is not None
        assert payload.company.corporate_id == "1000000000001"
        assert payload.signals.hiring.has_recruit_page is True
        assert payload.signals.tech.has_github is True
    finally:
        session.close()
