import asyncio
from datetime import UTC, datetime

from fastapi import HTTPException

from app.api.company import refresh_signals
from app.crawlers.website_signal_crawler import CrawledSignals, crawl_website_signals
from app.core.db import Base, SessionLocal, engine
from app.models.company import Company
from app.models.search_index import SearchIndex
from app.models.signal import Signal


def setup_module() -> None:
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        session.query(SearchIndex).delete()
        session.query(Signal).delete()
        session.query(Company).delete()

        session.add(
            Company(
                corporate_id="2000000000001",
                legal_name="株式会社Signal",
                normalized_name="SIGNAL",
                address="東京都港区1-2-3",
                prefecture="東京都",
                website="https://signal.example.com",
                industry="IT",
                is_listed=False,
            )
        )
        session.commit()
    finally:
        session.close()


def test_crawler_detects_recruit_blog_github_and_recent_update(monkeypatch) -> None:
    responses = {
        "https://signal.example.com": (
            """
            <html>
                <body>
                    <h1>エンジニア募集</h1>
                    <p>2026/03/01 更新</p>
                    <a href="/blog">Tech Blog</a>
                    <a href="https://github.com/example-org">GitHub</a>
                </body>
            </html>
            """,
            200,
        ),
        "https://signal.example.com/recruit": ("<html>採用情報</html>", 200),
        "https://signal.example.com/careers": (None, 404),
        "https://signal.example.com/jobs": (None, 404),
    }

    def fake_fetch_page(url: str) -> tuple[str | None, int | None]:
        return responses.get(url, (None, 404))

    monkeypatch.setattr("app.crawlers.website_signal_crawler.fetch_page", fake_fetch_page)

    result = crawl_website_signals("https://signal.example.com")

    assert result.has_recruit_page is True
    assert result.has_keywords is True
    assert result.recent_update is True
    assert result.has_engineer_keyword is True
    assert result.has_blog is True
    assert result.has_github is True
    assert result.checked_at is not None


def test_refresh_signals_endpoint_updates_company_signals(monkeypatch) -> None:
    checked_at = datetime(2026, 3, 19, 2, 0, tzinfo=UTC)

    def fake_crawl_website_signals(website: str | None) -> CrawledSignals:
        assert website == "https://signal.example.com"
        return CrawledSignals(
            has_recruit_page=True,
            has_keywords=True,
            recent_update=True,
            has_engineer_keyword=True,
            has_blog=True,
            has_github=False,
            checked_at=checked_at,
        )

    monkeypatch.setattr(
        "app.services.signal_service.crawl_website_signals",
        fake_crawl_website_signals,
    )

    payload = asyncio.run(refresh_signals("2000000000001"))

    assert payload.company.corporate_id == "2000000000001"
    assert payload.signals.hiring.has_recruit_page is True
    assert payload.signals.hiring.has_keywords is True
    assert payload.signals.hiring.recent_update is True
    assert payload.signals.tech.has_blog is True
    assert payload.signals.tech.has_github is False
    assert payload.signals.checked_at == checked_at.replace(tzinfo=None)


def test_refresh_signals_endpoint_returns_404_for_missing_company() -> None:
    try:
        asyncio.run(refresh_signals("9999999999999"))
    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == "Company not found"
    else:
        raise AssertionError("Expected HTTPException for missing company")
