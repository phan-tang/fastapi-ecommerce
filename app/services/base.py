from fastapi import HTTPException
from starlette import status
from uuid import UUID
from datetime import datetime
from schemas import User, UserType


class BaseService:

    def show(self, id: UUID):
        return self.repository.find_element_by_key('id', id)
        
    def delete(self, item):
        item.is_deleted = True
        item.deleted_at = datetime.utcnow()
        return self.repository.soft_delete(item)

    def validate_data_from_form_request(self, data, unique_fields):
        for key in unique_fields:
            self.check_unique_field(key, getattr(data, key))
        return data

    def check_unique_field(self, key: str, value: str):
        found_item = self.repository.find_element_by_key(key, value, True)
        if found_item:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"{key.replace('_', ' ').capitalize()} already exists")

    def check_admin_permission(self, user: User):
        return (user.user_type == UserType.ADMIN.value and not user.is_deleted)

    def access_denied_exception(self, detail="Access denied"):
        return HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail)

    def not_found_exception(self, detail="This item doesn't exist"):
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail)

    def token_exception(self):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password is incorrect",
            headers={"WWW-Authenticate": "Bearer"})
