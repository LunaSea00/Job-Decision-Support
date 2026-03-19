from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Company(Base):
    __tablename__ = "companies"

    corporate_id: Mapped[str] = mapped_column(String(13), primary_key=True)
    legal_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    normalized_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    prefecture: Mapped[str | None] = mapped_column(String(32), nullable=True, index=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(128), nullable=True)
    is_listed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    signal = relationship("Signal", back_populates="company", uselist=False, cascade="all, delete-orphan")
