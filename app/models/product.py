from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID
from sqlalchemy import func

from datetime import datetime
from .request import BaseQueryRequest, BaseFormRequest
from schemas import ProductStatus, Brand, Category, Review, DiscountType, SubCategory

class ProductFormRequestModel(BaseFormRequest):
    brand_id: UUID
    category_id: UUID
    product_name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=255)
    price: float = Field(min=0)
    quantity: int = Field(min=0, default=0)
    main_image_link: Optional[str] = Field(min_length=1, max_length=100, default=None)
    image_links: Optional[str] = Field(min_length=1, max_length=255, default=None)
    product_status: Optional[ProductStatus] = Field(default=ProductStatus.INVISIBLE)
    
    def get_unique_fields(self):
        return ['product_name']

class BaseProductViewModel(BaseModel):
    id: UUID
    brand_id: UUID
    category_id: UUID
    product_name: str
    description: str
    price: float
    quantity: int
    main_image_link: str | None = None
    image_links: str | None = None
    is_deleted: bool | None = None
    product_status: ProductStatus | None = None
    
    class Config:
        from_attributes = True


class ProductViewModel(BaseModel):
    id: UUID
    brand_name: str
    category_name: str
    product_name: str
    description: str
    price: float
    quantity: int
    average_rating: float
    discount_value: float | None = None
    discount_percentage: float | None = None
    discount_type: DiscountType | None = None
    final_price: float | None = None
    main_image_link: str | None = None
    image_links: str | None = None
    product_status: ProductStatus | None = None
    sub_categories: list = []

    class Config:
        from_attributes = True


class ProductQueryRequest(BaseQueryRequest):
    product_status: Optional[str] = Field(default=None)
    brand_name: Optional[str] = Field(default=None)
    category_name: Optional[str] = Field(default=None)
    sub_category_name: Optional[str] = Field(default=None)

    def get_sort_fields(self):
        return ['id', 'product_name', 'discount_value', 'final_price', 'average_rating']

    def get_filter_fields(self):
        return ['product_status', 'brand_name', 'category_name', 'sub_category_name']

    def get_search_fields(self):
        return ['product_name', 'description']

    def get_enum_fields(self):
        return {"product_status": ProductStatus}

    def get_other_table_attribute(self):
        return {
            "brand_name": Brand,
            "category_name": Category,
            "final_price": None,
            "average_rating": None,
            "discount_value": None,
            "sub_category_name": SubCategory
        }