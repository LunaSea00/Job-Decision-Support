from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PolicySignals(BaseModel):
    dx: bool | None = None
    tokyo_whitelist: bool | None = None


class HiringSignals(BaseModel):
    has_recruit_page: bool | None = None
    has_keywords: bool | None = None
    recent_update: bool | None = None


class TechSignals(BaseModel):
    has_engineer_keyword: bool | None = None
    has_blog: bool | None = None
    has_github: bool | None = None


class SignalResponse(BaseModel):
    policy: PolicySignals
    hiring: HiringSignals
    tech: TechSignals
    checked_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)
