from fastapi import Depends, Request
from datetime import datetime
from repositories import ReviewRepository

from models import ReviewFormRequestModel, ReviewQueryRequest
from schemas import Review
from .base_auth import BaseAuthService
from .query_params import QueryParamsService

class ReviewService(QueryParamsService):
    repository: ReviewRepository

    def __init__(self, repository: ReviewRepository = Depends()) -> None:
        self.repository = repository

    def list(self, request: Request):
        query_params = self.transform_request_query_params(request.url)
        params = ReviewQueryRequest(**dict(query_params))
        params = self.transform_query_params(params)
        return self.repository.list(params)

    def create(self, request: ReviewFormRequestModel):
        new_product = self.validate_data_from_form_request(Review(**dict(request)), request.get_unique_fields())
        new_product.created_at = datetime.utcnow()
        return self.repository.create(new_product)

    def update(self, old_product: Review, request: ReviewFormRequestModel):
        product = self.validate_data_from_form_request(Review(**dict(request)), request.get_unique_fields())
        product.id = old_product.id
        product.updated_at = datetime.utcnow()
        return self.repository.update(product)