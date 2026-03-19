from urllib.parse import urlparse


def extract_domain(url: str | None) -> str | None:
    if not url:
        return None

    parsed = urlparse(url)
    return parsed.netloc or None
