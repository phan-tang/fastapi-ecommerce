from sqlalchemy import Column, String, Numeric
from .base_entity import BaseEntity
from database import Base

class Brand(Base, BaseEntity):
    __tablename__ = "brands"

    brand_name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=False)
    default_image_link = Column(String(255))
    dark_theme_image_link = Column(String(255))