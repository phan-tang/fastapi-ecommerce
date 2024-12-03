from sqlalchemy import Column, String, Enum, Numeric, Boolean
from database import Base
from .base_enum import BaseEnum
from .base_entity import BaseEntity

class UserType(BaseEnum):
    ADMIN = 'A'
    USER = 'U'

class User(Base, BaseEntity):
    __tablename__ = "users"

    email = Column(String(255), nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    password = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=0)
    user_type = Column(Enum(UserType), default=UserType.USER)