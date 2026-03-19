from functools import lru_cache
import os


class Settings:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "company-info-mvp")
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")
        self.request_timeout_seconds = int(os.getenv("REQUEST_TIMEOUT_SECONDS", "8"))


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
