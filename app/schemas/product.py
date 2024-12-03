from sqlalchemy import Column, String, Numeric, Uuid, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .base_enum import BaseEnum
from .base_entity import BaseEntity
from database import Base

class ProductStatus(BaseEnum):
    INVISIBLE = 'I'
    VISIBLE = 'V'

class Product(Base, BaseEntity):
    __tablename__ = "products"

    brand_id = Column(Uuid, ForeignKey('brands.id'), nullable=False)
    category_id = Column(Uuid, ForeignKey('categories.id'), nullable=False)
    product_name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Numeric, nullable=False)
    quantity = Column(Numeric, default=0)
    main_image_link = Column(String(100))
    image_links = Column(String(255))
    product_status = Column(Enum(ProductStatus), default=ProductStatus.INVISIBLE)

    brand = relationship('Brand')
    category = relationship('Category')