from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.signal import Signal
from app.schemas.company import CompanyBase, CompanyDetailResponse
from app.schemas.signal import HiringSignals, PolicySignals, SignalResponse, TechSignals


def build_signal_response(signal: Signal | None) -> SignalResponse:
    return SignalResponse(
        policy=PolicySignals(
            dx=getattr(signal, "dx", None),
            tokyo_whitelist=getattr(signal, "tokyo_whitelist", None),
        ),
        hiring=HiringSignals(
            has_recruit_page=getattr(signal, "has_recruit_page", None),
            has_keywords=getattr(signal, "has_keywords", None),
            recent_update=getattr(signal, "recent_update", None),
        ),
        tech=TechSignals(
            has_engineer_keyword=getattr(signal, "has_engineer_keyword", None),
            has_blog=getattr(signal, "has_blog", None),
            has_github=getattr(signal, "has_github", None),
        ),
        checked_at=getattr(signal, "checked_at", None),
    )


def get_company_detail(db: Session, corporate_id: str) -> CompanyDetailResponse | None:
    company = db.get(Company, corporate_id)
    if company is None:
        return None

    signal = db.get(Signal, corporate_id)
    return CompanyDetailResponse(
        company=CompanyBase.model_validate(company),
        signals=build_signal_response(signal),
    )
