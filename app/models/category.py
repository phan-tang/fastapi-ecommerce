from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from .request import BaseQueryRequest, BaseFormRequest


class CategoryFormRequestModel(BaseFormRequest):
    category_name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=255)

    def get_unique_fields(self):
        return ['category_name']

class BaseCategoryViewModel(BaseModel):
    id: UUID
    category_name: str
    description: str
    is_deleted: bool | None = None

    class Config:
        from_attributes = True


class CategoryViewModel(BaseCategoryViewModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        from_attributes = True


class CategoryQueryRequest(BaseQueryRequest):

    def get_sort_fields(self):
        return ['id', 'category_name', 'description']

    def get_search_fields(self):
        return ['category_name', 'description']