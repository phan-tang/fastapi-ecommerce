from fastapi import Depends, Request
from datetime import datetime
from repositories import DiscountRepository

from models import DiscountFormRequestModel, DiscountQueryRequest
from schemas import Discount
from .base_auth import BaseAuthService
from .query_params import QueryParamsService

class DiscountService(QueryParamsService):
    repository: DiscountRepository

    def __init__(self, repository: DiscountRepository = Depends()) -> None:
        self.repository = repository

    def list(self, request: Request):
        query_params = self.transform_request_query_params(request.url)
        params = DiscountQueryRequest(**dict(query_params))
        params = self.transform_query_params(params)
        return self.repository.list(params)

    def create(self, request: DiscountFormRequestModel):
        new_discount = self.validate_data_from_form_request(Discount(**dict(request)), request.get_unique_fields())
        new_discount.created_at = datetime.utcnow()
        return self.repository.create(new_discount)

    def update(self, old_discount: Discount, request: DiscountFormRequestModel):
        discount = self.validate_data_from_form_request(Discount(**dict(request)), request.get_unique_fields())
        discount.id = old_discount.id
        discount.updated_at = datetime.utcnow()
        return self.repository.update(discount)