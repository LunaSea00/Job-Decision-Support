from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class SearchIndex(Base):
    __tablename__ = "search_index"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    corporate_id: Mapped[str] = mapped_column(String(13), ForeignKey("companies.corporate_id"), nullable=False, index=True)
    legal_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    normalized_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    aliases: Mapped[str | None] = mapped_column(String(512), nullable=True)
    website_domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    prefecture: Mapped[str | None] = mapped_column(String(32), nullable=True)
