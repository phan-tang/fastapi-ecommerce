from sqlalchemy import Column, String, Numeric
from .base_entity import BaseEntity
from database import Base

class Category(Base, BaseEntity):
    __tablename__ = "categories"

    category_name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255), nullable=False)