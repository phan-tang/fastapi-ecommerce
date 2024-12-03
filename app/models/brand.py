from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from .request import BaseQueryRequest, BaseFormRequest


class BrandFormRequestModel(BaseFormRequest):
    brand_name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=255)
    default_image_link: Optional[str] = Field(min_length=1, max_length=255, default=None)
    dark_theme_image_link: Optional[str] = Field(min_length=1, max_length=255, default=None)
    
    def get_unique_fields(self):
        return ['brand_name']

class BaseBrandViewModel(BaseModel):
    id: UUID
    brand_name: str
    description: str
    default_image_link: str | None = None
    dark_theme_image_link: str | None = None
    is_deleted: bool | None = None
    
    class Config:
        from_attributes = True


class BrandViewModel(BaseBrandViewModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        from_attributes = True


class BrandQueryRequest(BaseQueryRequest):

    def get_sort_fields(self):
        return ['id', 'brand_name', 'description']

    def get_search_fields(self):
        return ['brand_name', 'description']