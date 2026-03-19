from dataclasses import dataclass
from datetime import datetime, UTC
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from app.core.config import settings

RECRUIT_PATHS = ("/recruit", "/careers", "/jobs")
BLOG_HINTS = ("/blog", "/tech", "/engineer")
HIRING_KEYWORDS = ("採用", "募集", "求人", "エンジニア", "中途採用", "新卒採用")
ENGINEER_KEYWORDS = ("エンジニア", "engineer", "developers")
RECENT_YEAR_MARKERS = ("2024", "2025", "2026")


@dataclass
class CrawledSignals:
    dx: bool | None = None
    tokyo_whitelist: bool | None = None
    has_recruit_page: bool | None = None
    has_keywords: bool | None = None
    recent_update: bool | None = None
    has_engineer_keyword: bool | None = None
    has_blog: bool | None = None
    has_github: bool | None = None
    checked_at: datetime | None = None


def fetch_page(url: str) -> tuple[str | None, int | None]:
    try:
        response = requests.get(url, timeout=settings.request_timeout_seconds)
        return response.text, response.status_code
    except requests.RequestException:
        return None, None


def crawl_website_signals(website: str | None) -> CrawledSignals:
    if not website:
        return CrawledSignals(checked_at=datetime.now(UTC))

    html, status_code = fetch_page(website)
    if status_code != 200 or not html:
        return CrawledSignals(checked_at=datetime.now(UTC))

    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(" ", strip=True)
    lower_html = html.lower()

    has_recruit_page = False
    for path in RECRUIT_PATHS:
        _, recruit_status = fetch_page(urljoin(website, path))
        if recruit_status == 200:
            has_recruit_page = True
            break

    links = [link.get("href", "") for link in soup.find_all("a")]
    has_blog = any(hint in lower_html for hint in BLOG_HINTS) or any(
        any(hint in href.lower() for hint in BLOG_HINTS) for href in links
    )

    return CrawledSignals(
        has_recruit_page=has_recruit_page,
        has_keywords=any(keyword in page_text for keyword in HIRING_KEYWORDS),
        recent_update=any(marker in page_text for marker in RECENT_YEAR_MARKERS)
        or any(marker in lower_html for marker in ("更新日", "掲載日")),
        has_engineer_keyword=any(keyword in page_text.lower() for keyword in ENGINEER_KEYWORDS),
        has_blog=has_blog,
        has_github="github.com" in lower_html,
        checked_at=datetime.now(UTC),
    )
