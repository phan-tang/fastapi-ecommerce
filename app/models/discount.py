from pydantic import BaseModel, Field, field_validator, ValidationError 
from pydantic_core.core_schema import FieldValidationInfo

from typing import Optional
from uuid import UUID
from datetime import datetime
from .request import BaseQueryRequest, BaseFormRequest
from schemas import DiscountType

class DiscountFormRequestModel(BaseFormRequest):
    discount_name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=255)
    start_date: str = Field(default=datetime.today())
    end_date: Optional[str] = Field(default=None)
    discount_type: Optional[DiscountType] = Field(default=DiscountType.VALUE)
    discount_value: float = Field(min=0)

    @field_validator("discount_value")
    def check_valid_discount_value(cls, value, info: FieldValidationInfo):
        if info.data["discount_type"] == DiscountType.PERCENTAGE and value > 60:
            raise ValueError("Discount percentage must be less than or equal to 60")
        return value

class BaseDiscountViewModel(BaseModel):
    id: UUID
    discount_name: str
    description: str
    start_date: datetime
    end_date: datetime | None = None
    discount_type: DiscountType | None = None
    discount_value: float
    is_deleted: bool | None = None

    class Config:
        from_attributes = True


class DiscountViewModel(BaseDiscountViewModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        from_attributes = True


class DiscountQueryRequest(BaseQueryRequest):
    discount_type: Optional[str] = Field(default=None)

    def get_sort_fields(self):
        return ['id', 'discount_name', 'description']

    def get_filter_fields(self):
        return ['discount_type']

    def get_search_fields(self):
        return ['discount_name', 'description']

    def get_enum_fields(self):
        return {"discount_type": DiscountType}