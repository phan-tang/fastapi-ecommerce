from fastapi import Depends, Request
from datetime import datetime
from repositories import SubCategoryRepository

from models import SubCategoryFormRequestModel, SubCategoryQueryRequest
from schemas import SubCategory
from .base_auth import BaseAuthService
from .query_params import QueryParamsService

class SubCategoryService(QueryParamsService):
    repository: SubCategoryRepository

    def __init__(self, repository: SubCategoryRepository = Depends()) -> None:
        self.repository = repository

    def list(self, request: Request):
        query_params = self.transform_request_query_params(request.url)
        params = SubCategoryQueryRequest(**dict(query_params))
        params = self.transform_query_params(params)
        return self.repository.list(params)

    def create(self, request: SubCategoryFormRequestModel):
        new_sub_category = self.validate_data_from_form_request(SubCategory(**dict(request)), request.get_unique_fields())
        new_sub_category.created_at = datetime.utcnow()
        return self.repository.create(new_sub_category)

    def update(self, old_sub_category: SubCategory, request: SubCategoryFormRequestModel):
        sub_category = self.validate_data_from_form_request(SubCategory(**dict(request)), request.get_unique_fields())
        sub_category.id = old_sub_category.id
        sub_category.updated_at = datetime.utcnow()
        return self.repository.update(sub_category)