import re
import unicodedata

COMPANY_TOKENS = (
    "株式会社",
    "（株）",
    "(株)",
    "㈱",
)


def normalize_company_name(name: str) -> str:
    normalized = unicodedata.normalize("NFKC", name).strip()
    normalized = re.sub(r"\s+", "", normalized)

    for token in COMPANY_TOKENS:
        normalized = normalized.replace(token, "")

    return normalized.upper()
