from sqlalchemy import Column, String, Numeric, Uuid, ForeignKey
from .base_entity import BaseEntity
from database import Base

class SubCategory(Base, BaseEntity):
    __tablename__ = "sub_categories"

    sub_category_name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=False)

class ProductSubCategory(Base, BaseEntity):
    __tablename__ = "products_sub_categories"

    product_id = Column(Uuid, ForeignKey('products.id'), nullable=False)
    sub_category_id = Column(Uuid, ForeignKey('sub_categories.id'), nullable=False)