from pydantic import BaseModel, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from fastapi import Depends

from uuid import UUID
from datetime import datetime
from typing import Optional

from validators import PasswordValidator, EmailValidator
from schemas import UserType, User
from .request import BaseQueryRequest, BaseFormRequest

class UserFormRequestModel(BaseFormRequest):
    email: str = Field(min_length=1, max_length=255)
    username: str = Field(min_length=1, max_length=255)
    first_name: str = Field(min_length=1, max_length=255)
    last_name: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=8)
    user_type: Optional[UserType] = Field(default=UserType.USER)

    @field_validator("password")
    def check_valid_password(cls, value, info: FieldValidationInfo):
        return PasswordValidator(value).password

    @field_validator("email")
    def check_valid_email(cls, value, info: FieldValidationInfo):
        return EmailValidator(value).email

    def get_unique_fields(self):
        return ['username', 'email']

class BaseUserViewModel(BaseModel):
    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    is_deleted: bool | None = None
    user_type: UserType | None = None

    class Config:
        from_attributes = True


class UserViewModel(BaseUserViewModel):
    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None

    class Config:
        from_attributes = True


class UserQueryRequest(BaseQueryRequest):
    user_type: Optional[str] = Field(default=None)

    def get_sort_fields(self):
        return ['id', 'first_name', 'last_name', 'email', 'username', 'user_type']

    def get_filter_fields(self):
        return ['user_type']

    def get_search_fields(self):
        return ['first_name', 'last_name', 'email', 'username']

    def get_enum_fields(self):
        return {"user_type": UserType}
