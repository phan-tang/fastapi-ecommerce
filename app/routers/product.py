from fastapi import APIRouter, Request, Depends
from uuid import UUID
from typing import List

from models import ProductFormRequestModel, ProductViewModel, BaseProductViewModel
from services import ProductService, AuthService, oa2_bearer

import time

router = APIRouter(prefix="/products", tags=["Product"])

@router.get('', response_model=List[ProductViewModel])
async def get_products(
        request: Request,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: ProductService = Depends()):
    start_time = time.time()
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    result = service.list(request)
    print(f"Execution time: {time.time()-start_time}")
    return result

@router.get('/{product_id}', response_model=ProductViewModel | None)
async def get_product_by_id(
        product_id: UUID,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: ProductService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    product = service.show(product_id)
    if not product:
        raise service.not_found_exception()
    return product

@router.post('', response_model=BaseProductViewModel)
async def create_product(
        request: ProductFormRequestModel,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: ProductService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    result = service.create(request)
    return result

@router.put('/{product_id}', response_model=BaseProductViewModel)
async def update_product(
        product_id: UUID,
        request: ProductFormRequestModel,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: ProductService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    product = service.show(product_id)
    return service.update(product, request)

@router.delete('/{product_id}')
async def delete_product(
        product_id: UUID,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: ProductService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    product = service.show(product_id)
    if not product:
        raise service.not_found_exception()
    return service.delete(product)
