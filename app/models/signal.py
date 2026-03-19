from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Signal(Base):
    __tablename__ = "signals"

    corporate_id: Mapped[str] = mapped_column(String(13), ForeignKey("companies.corporate_id"), primary_key=True)
    dx: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    tokyo_whitelist: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    has_recruit_page: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    has_keywords: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    recent_update: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    has_engineer_keyword: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    has_blog: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    has_github: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    checked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    company = relationship("Company", back_populates="signal")
