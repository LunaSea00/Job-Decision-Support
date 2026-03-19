from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.company import Company
from app.models.search_index import SearchIndex
from app.schemas.search import SearchResultItem
from app.utils.normalizer import normalize_company_name


def search_companies(db: Session, query: str) -> list[SearchResultItem]:
    normalized_query = normalize_company_name(query)
    alias_pattern = f"%{normalized_query}%"

    # Search against both the canonical normalized name and alias text to keep
    # duplicate-name disambiguation practical without a complex full-text index.
    stmt = (
        select(Company)
        .join(SearchIndex, SearchIndex.corporate_id == Company.corporate_id)
        .where(
            or_(
                Company.normalized_name.contains(normalized_query),
                SearchIndex.normalized_name.contains(normalized_query),
                SearchIndex.aliases.ilike(alias_pattern),
            )
        )
        .order_by(Company.is_listed.desc(), Company.prefecture.asc(), Company.corporate_id.asc())
    )
    companies = db.scalars(stmt).all()
    return [SearchResultItem.model_validate(company) for company in companies]
