from pydantic import BaseModel, ConfigDict


class SearchResultItem(BaseModel):
    corporate_id: str
    legal_name: str
    prefecture: str | None = None
    website: str | None = None
    industry: str | None = None
    is_listed: bool | None = None

    model_config = ConfigDict(from_attributes=True)
