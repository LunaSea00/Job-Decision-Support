from fastapi import APIRouter, Query

from app.core.db import SessionLocal
from app.schemas.search import SearchResultItem
from app.services.search_service import search_companies

router = APIRouter(tags=["search"])


@router.get("/search", response_model=list[SearchResultItem])
async def search(q: str = Query(..., min_length=1)) -> list[SearchResultItem]:
    with SessionLocal() as db:
        return search_companies(db=db, query=q)
