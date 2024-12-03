from fastapi import Depends, Request
from datetime import datetime
from repositories import CategoryRepository

from models import CategoryFormRequestModel, CategoryQueryRequest
from schemas import Category
from .base_auth import BaseAuthService
from .query_params import QueryParamsService

class CategoryService(QueryParamsService):
    repository: CategoryRepository

    def __init__(self, repository: CategoryRepository = Depends()) -> None:
        self.repository = repository

    def list(self, request: Request):
        query_params = self.transform_request_query_params(request.url)
        params = CategoryQueryRequest(**dict(query_params))
        params = self.transform_query_params(params)
        return self.repository.list(params)

    def create(self, request: CategoryFormRequestModel):
        new_category = self.validate_data_from_form_request(Category(**dict(request)), request.get_unique_fields())
        new_category.created_at = datetime.utcnow()
        return self.repository.create(new_category)

    def update(self, old_category: Category, request: CategoryFormRequestModel):
        category = self.validate_data_from_form_request(Category(**dict(request)), request.get_unique_fields())
        category.id = old_category.id
        category.updated_at = datetime.utcnow()
        return self.repository.update(category)