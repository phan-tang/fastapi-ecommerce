from fastapi import Depends, Request
from datetime import datetime
from repositories import BrandRepository

from models import BrandFormRequestModel, BrandQueryRequest
from schemas import Brand
from .base_auth import BaseAuthService
from .query_params import QueryParamsService

class BrandService(QueryParamsService):
    repository: BrandRepository

    def __init__(self, repository: BrandRepository = Depends()) -> None:
        self.repository = repository

    def list(self, request: Request):
        query_params = self.transform_request_query_params(request.url)
        params = BrandQueryRequest(**dict(query_params))
        params = self.transform_query_params(params)
        return self.repository.list(params)

    def create(self, request: BrandFormRequestModel):
        new_brand = self.validate_data_from_form_request(Brand(**dict(request)), request.get_unique_fields())
        new_brand.created_at = datetime.utcnow()
        return self.repository.create(new_brand)

    def update(self, old_brand: Brand, request: BrandFormRequestModel):
        brand = self.validate_data_from_form_request(Brand(**dict(request)), request.get_unique_fields())
        brand.id = old_brand.id
        brand.updated_at = datetime.utcnow()
        return self.repository.update(brand)