from pydantic import BaseModel, ConfigDict

from app.schemas.signal import SignalResponse


class CompanyBase(BaseModel):
    corporate_id: str
    legal_name: str
    address: str | None = None
    prefecture: str | None = None
    website: str | None = None
    industry: str | None = None
    is_listed: bool | None = None

    model_config = ConfigDict(from_attributes=True)


class CompanyDetailResponse(BaseModel):
    company: CompanyBase
    signals: SignalResponse
