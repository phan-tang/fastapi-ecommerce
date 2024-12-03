from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from .request import BaseQueryRequest, BaseFormRequest


class SubCategoryFormRequestModel(BaseFormRequest):
    sub_category_name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=255)

    def get_unique_fields(self):
        return ['sub_category_name']

class BaseSubCategoryViewModel(BaseModel):
    id: UUID
    sub_category_name: str
    description: str
    is_deleted: bool | None = None

    class Config:
        from_attributes = True


class SubCategoryViewModel(BaseSubCategoryViewModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        from_attributes = True


class SubCategoryQueryRequest(BaseQueryRequest):

    def get_sort_fields(self):
        return ['id', 'sub_category_name', 'description']

    def get_search_fields(self):
        return ['sub_category_name', 'description']