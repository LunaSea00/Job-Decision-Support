from fastapi import FastAPI

from app.api.company import router as company_router
from app.api.search import router as search_router
from app.core.config import settings
from app.core.db import Base, engine


# Create tables on startup for the MVP so the app can run without migrations.
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.app_name)
app.include_router(search_router)
app.include_router(company_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
