from fastapi import APIRouter, HTTPException

from app.core.db import SessionLocal
from app.schemas.company import CompanyDetailResponse
from app.services.company_service import get_company_detail
from app.services.signal_service import refresh_company_signals

router = APIRouter(tags=["company"])


@router.get("/company/{corporate_id}", response_model=CompanyDetailResponse)
async def company_detail(corporate_id: str) -> CompanyDetailResponse:
    with SessionLocal() as db:
        detail = get_company_detail(db=db, corporate_id=corporate_id)
        if detail is None:
            raise HTTPException(status_code=404, detail="Company not found")
        return detail


@router.post("/company/{corporate_id}/refresh-signals", response_model=CompanyDetailResponse)
async def refresh_signals(corporate_id: str) -> CompanyDetailResponse:
    with SessionLocal() as db:
        detail = refresh_company_signals(db=db, corporate_id=corporate_id)
        if detail is None:
            raise HTTPException(status_code=404, detail="Company not found")
        return detail
