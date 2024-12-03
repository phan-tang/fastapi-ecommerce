from fastapi import APIRouter, Request, Depends
from uuid import UUID
from typing import List

from models import BrandFormRequestModel, BrandViewModel, BaseBrandViewModel
from services import BrandService, AuthService, oa2_bearer

import time

router = APIRouter(prefix="/brands", tags=["Brand"])

@router.get('', response_model=List[BrandViewModel])
async def get_brands(
        request: Request,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: BrandService = Depends()):
    start_time = time.time()
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    result = service.list(request)
    print(f"Execution time: {time.time()-start_time}")
    return result

@router.get('/{brand_id}', response_model=BrandViewModel | None)
async def get_brand_by_id(
        brand_id: UUID,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: BrandService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    brand = service.show(brand_id)
    if not brand:
        raise service.not_found_exception()
    return brand

@router.post('', response_model=BaseBrandViewModel)
async def create_brand(
        request: BrandFormRequestModel,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: BrandService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    result = service.create(request)
    return result

@router.put('/{brand_id}', response_model=BaseBrandViewModel)
async def update_brand(
        brand_id: UUID,
        request: BrandFormRequestModel,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: BrandService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    brand = service.show(brand_id)
    return service.update(brand, request)

@router.delete('/{brand_id}')
async def delete_brand(
        brand_id: UUID,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: BrandService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    brand = service.show(brand_id)
    if not brand:
        raise service.not_found_exception()
    return service.delete(brand)
