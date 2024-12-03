from fastapi import Depends, Request
from datetime import datetime
from repositories import UserRepository

from models import UserQueryRequest, UserFormRequestModel
from schemas import User
from .base_auth import BaseAuthService
from .query_params import QueryParamsService

class UserService(BaseAuthService, QueryParamsService):
    repository: UserRepository

    def __init__(self, repository: UserRepository = Depends()) -> None:
        self.repository = repository

    def list(self, request: Request):
        query_params = self.transform_request_query_params(request.url)
        params = UserQueryRequest(**dict(query_params))
        params = self.transform_query_params(params)
        return self.repository.list(params)

    def create(self, request: UserFormRequestModel):
        new_user = self.validate_data_from_form_request(User(**dict(request)), request.get_unique_fields())
        new_user.password = self.get_password_hash(request.password)
        new_user.created_at = datetime.utcnow()
        return self.repository.create(new_user)

    def update(self, old_user: User, request: UserFormRequestModel):
        user = self.validate_data_from_form_request(User(**dict(request)), request.get_unique_fields())
        user.id = old_user.id
        user.password = self.get_password_hash(request.password)
        user.updated_at = datetime.utcnow()
        return self.repository.update(user)
