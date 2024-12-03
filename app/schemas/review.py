from sqlalchemy import Column, String, Numeric, Uuid, ForeignKey, Enum
from sqlalchemy.orm import relationship

from .base_enum import BaseEnum
from .base_entity import BaseEntity
from database import Base

class ReviewStatus(BaseEnum):
    INVISIBLE = 'I'
    VISIBLE = 'V'

class Review(Base, BaseEntity):
    __tablename__ = "reviews"

    product_id = Column(Uuid, ForeignKey('products.id'), nullable=False)
    user_id = Column(Uuid, ForeignKey('users.id'), nullable=False)
    content = Column(String(255), nullable=False)
    rating = Column(Numeric, nullable=False)
    review_status = Column(Enum(ReviewStatus), default=ReviewStatus.INVISIBLE)

    product = relationship('Product')
    user = relationship('User')