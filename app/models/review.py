from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from datetime import datetime
from .request import BaseQueryRequest, BaseFormRequest
from schemas import ReviewStatus, User

class ReviewFormRequestModel(BaseFormRequest):
    product_id: UUID
    user_id: UUID
    content: str = Field(min_length=1, max_length=255)
    rating: int = Field(min=1, default=5)
    review_status: Optional[ReviewStatus] = Field(default=ReviewStatus.INVISIBLE)

class BaseReviewViewModel(BaseModel):
    id: UUID
    product_id: UUID
    user_id: UUID
    content: str
    rating: float
    is_deleted: bool | None = None
    review_status: ReviewStatus | None = None
    
    class Config:
        from_attributes = True


class ReviewViewModel(BaseReviewViewModel):
    email: str
    full_name: str
    created_at: datetime | None = None
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class ReviewQueryRequest(BaseQueryRequest):
    review_status: Optional[str] = Field(default=None)
    product_id: Optional[str] = Field(default=None)
    user_id: Optional[str] = Field(default=None)
    rating: Optional[str] = Field(default=None)

    def get_sort_fields(self):
        return ['id', 'review_name', 'rating']

    def get_filter_fields(self):
        return ['review_status', 'product_id', 'user_id', 'rating']

    def get_search_fields(self):
        return ['review_name', 'content']

    def get_numeric_fields(self):
        return ['rating']

    def get_enum_fields(self):
        return {"review_status": ReviewStatus}