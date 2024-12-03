from fastapi import APIRouter, Request, Depends
from uuid import UUID
from typing import List

from models import DiscountFormRequestModel, DiscountViewModel, BaseDiscountViewModel
from services import DiscountService, AuthService, oa2_bearer

import time

router = APIRouter(prefix="/discounts", tags=["Discount"])

@router.get('', response_model=List[DiscountViewModel])
async def get_discounts(
        request: Request,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: DiscountService = Depends()):
    start_time = time.time()
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    result = service.list(request)
    print(f"Execution time: {time.time()-start_time}")
    return result

@router.get('/{discount_id}', response_model=DiscountViewModel | None)
async def get_discount_by_id(
        discount_id: UUID,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: DiscountService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    discount = service.show(discount_id)
    if not discount:
        raise service.not_found_exception()
    return discount

@router.post('', response_model=BaseDiscountViewModel)
async def create_discount(
        request: DiscountFormRequestModel,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: DiscountService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    result = service.create(request)
    return result

@router.put('/{discount_id}', response_model=BaseDiscountViewModel)
async def update_discount(
        discount_id: UUID,
        request: DiscountFormRequestModel,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: DiscountService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    discount = service.show(discount_id)
    return service.update(discount, request)

@router.delete('/{discount_id}')
async def delete_discount(
        discount_id: UUID,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: DiscountService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    discount = service.show(discount_id)
    if not discount:
        raise service.not_found_exception()
    return service.delete(discount)
