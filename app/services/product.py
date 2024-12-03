from fastapi import Depends, Request
from datetime import datetime
from repositories import ProductRepository

from models import ProductFormRequestModel, ProductQueryRequest
from schemas import Product
from .base_auth import BaseAuthService
from .query_params import QueryParamsService

class ProductService(QueryParamsService):
    repository: ProductRepository

    def __init__(self, repository: ProductRepository = Depends()) -> None:
        self.repository = repository

    def list(self, request: Request):
        query_params = self.transform_request_query_params(request.url)
        params = ProductQueryRequest(**dict(query_params))
        params = self.transform_query_params(params)
        return self.repository.list(params)

    def create(self, request: ProductFormRequestModel):
        new_product = self.validate_data_from_form_request(Product(**dict(request)), request.get_unique_fields())
        new_product.created_at = datetime.utcnow()
        return self.repository.create(new_product)

    def update(self, old_product: Product, request: ProductFormRequestModel):
        product = self.validate_data_from_form_request(Product(**dict(request)), request.get_unique_fields())
        product.id = old_product.id
        product.updated_at = datetime.utcnow()
        return self.repository.update(product)