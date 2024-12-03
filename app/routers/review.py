from fastapi import APIRouter, Request, Depends
from uuid import UUID
from typing import List

from models import ReviewFormRequestModel, ReviewViewModel, BaseReviewViewModel
from services import ReviewService, AuthService, oa2_bearer

import time

router = APIRouter(prefix="/reviews", tags=["Review"])

@router.get('', response_model=List[ReviewViewModel])
async def get_reviews(
        request: Request,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: ReviewService = Depends()):
    start_time = time.time()
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    result = service.list(request)
    print(f"Execution time: {time.time()-start_time}")
    return result

@router.get('/{review_id}', response_model=ReviewViewModel | None)
async def get_review_by_id(
        review_id: UUID,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: ReviewService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    review = service.show(review_id)
    if not review:
        raise service.not_found_exception()
    return review

@router.post('', response_model=BaseReviewViewModel)
async def create_review(
        request: ReviewFormRequestModel,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: ReviewService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    result = service.create(request)
    return result

@router.put('/{review_id}', response_model=BaseReviewViewModel)
async def update_review(
        review_id: UUID,
        request: ReviewFormRequestModel,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: ReviewService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    review = service.show(review_id)
    return service.update(review, request)

@router.delete('/{review_id}')
async def delete_review(
        review_id: UUID,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: ReviewService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    review = service.show(review_id)
    if not review:
        raise service.not_found_exception()
    return service.delete(review)
