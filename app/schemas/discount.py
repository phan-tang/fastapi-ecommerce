from sqlalchemy import Column, String, Enum, Numeric, Boolean, DateTime, Uuid, ForeignKey
from database import Base
from .base_enum import BaseEnum
from .base_entity import BaseEntity

class DiscountType(BaseEnum):
    PERCENTAGE = 'P'
    VALUE = 'V'

class Discount(Base, BaseEntity):
    __tablename__ = "discounts"

    discount_name = Column(String(255), nullable=False, unique=True)
    description = Column(String(255), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, default=None)
    discount_type = Column(Enum(DiscountType), default=DiscountType.VALUE)
    discount_value = Column(Numeric, nullable=False)
    
class ProductDiscount(Base, BaseEntity):
    __tablename__ = "products_discounts"

    product_id = Column(Uuid, ForeignKey('products.id'), nullable=False)
    discount_id = Column(Uuid, ForeignKey('discounts.id'), nullable=False)