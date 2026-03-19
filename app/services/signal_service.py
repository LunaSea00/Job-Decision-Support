from sqlalchemy.orm import Session

from app.crawlers.website_signal_crawler import crawl_website_signals
from app.models.company import Company
from app.models.signal import Signal
from app.services.company_service import get_company_detail


def refresh_company_signals(db: Session, corporate_id: str):
    company = db.get(Company, corporate_id)
    if company is None:
        return None

    crawled = crawl_website_signals(company.website)
    signal = db.get(Signal, corporate_id)
    if signal is None:
        signal = Signal(corporate_id=corporate_id)
        db.add(signal)

    # Keep the write path explicit so this stays easy to audit and extend.
    signal.dx = crawled.dx
    signal.tokyo_whitelist = crawled.tokyo_whitelist
    signal.has_recruit_page = crawled.has_recruit_page
    signal.has_keywords = crawled.has_keywords
    signal.recent_update = crawled.recent_update
    signal.has_engineer_keyword = crawled.has_engineer_keyword
    signal.has_blog = crawled.has_blog
    signal.has_github = crawled.has_github
    signal.checked_at = crawled.checked_at

    db.commit()
    db.refresh(signal)
    return get_company_detail(db=db, corporate_id=corporate_id)
