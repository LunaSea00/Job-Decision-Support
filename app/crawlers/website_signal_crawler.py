from dataclasses import dataclass
from datetime import UTC, datetime
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from app.core.config import settings

RECRUIT_PATHS = ("/recruit", "/careers", "/jobs")
BLOG_HINTS = ("/blog", "/tech", "/engineer")
HIRING_KEYWORDS = ("採用", "募集", "求人", "エンジニア", "中途採用", "新卒採用")
ENGINEER_KEYWORDS = ("エンジニア", "engineer", "developers")
RECENT_TEXT_MARKERS = ("更新", "更新日", "掲載", "掲載日", "投稿日", "news", "お知らせ")


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


def _collect_links(soup: BeautifulSoup) -> list[str]:
    return [link.get("href", "") for link in soup.find_all("a") if link.get("href")]


def _contains_any(text: str, needles: tuple[str, ...]) -> bool:
    return any(needle in text for needle in needles)


def _recent_year_markers() -> tuple[str, ...]:
    current_year = datetime.now(UTC).year
    return tuple(str(year) for year in range(current_year - 1, current_year + 1))


def _has_recruit_page(website: str, links: list[str]) -> bool:
    if any(_contains_any(link.lower(), RECRUIT_PATHS) for link in links):
        return True

    for path in RECRUIT_PATHS:
        _, recruit_status = fetch_page(urljoin(website, path))
        if recruit_status == 200:
            return True
    return False


def _has_blog(lower_html: str, links: list[str]) -> bool:
    return _contains_any(lower_html, BLOG_HINTS) or any(
        _contains_any(link.lower(), BLOG_HINTS) for link in links
    )


def _has_recent_update(page_text: str, lower_html: str) -> bool:
    return (
        _contains_any(page_text, _recent_year_markers())
        or _contains_any(page_text, RECENT_TEXT_MARKERS)
        or _contains_any(lower_html, RECENT_TEXT_MARKERS)
    )


def _has_github(lower_html: str, links: list[str]) -> bool:
    return "github.com" in lower_html or any("github.com" in link.lower() for link in links)


def crawl_website_signals(website: str | None) -> CrawledSignals:
    if not website:
        return CrawledSignals(checked_at=datetime.now(UTC))

    html, status_code = fetch_page(website)
    if status_code != 200 or not html:
        return CrawledSignals(checked_at=datetime.now(UTC))

    soup = BeautifulSoup(html, "html.parser")
    page_text = soup.get_text(" ", strip=True)
    lower_html = html.lower()
    lower_text = page_text.lower()
    links = _collect_links(soup)

    return CrawledSignals(
        has_recruit_page=_has_recruit_page(website, links),
        has_keywords=any(keyword in page_text for keyword in HIRING_KEYWORDS),
        recent_update=_has_recent_update(page_text, lower_html),
        has_engineer_keyword=any(keyword in lower_text for keyword in ENGINEER_KEYWORDS),
        has_blog=_has_blog(lower_html, links),
        has_github=_has_github(lower_html, links),
        checked_at=datetime.now(UTC),
    )
