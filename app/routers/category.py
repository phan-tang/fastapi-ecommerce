from fastapi import APIRouter, Request, Depends
from uuid import UUID
from typing import List

from models import CategoryFormRequestModel, CategoryViewModel, BaseCategoryViewModel
from services import CategoryService, AuthService, oa2_bearer

import time

router = APIRouter(prefix="/categories", tags=["Category"])

@router.get('', response_model=List[CategoryViewModel])
async def get_categories(
        request: Request,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: CategoryService = Depends()):
    start_time = time.time()
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    result = service.list(request)
    print(f"Execution time: {time.time()-start_time}")
    return result

@router.get('/{category_id}', response_model=CategoryViewModel | None)
async def get_category_by_id(
        category_id: UUID,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: CategoryService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    category = service.show(category_id)
    if not category:
        raise service.not_found_exception()
    return category

@router.post('', response_model=BaseCategoryViewModel)
async def create_category(
        request: CategoryFormRequestModel,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: CategoryService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    result = service.create(request)
    return result

@router.put('/{category_id}', response_model=BaseCategoryViewModel)
async def update_category(
        category_id: UUID,
        request: CategoryFormRequestModel,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: CategoryService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    category = service.show(category_id)
    return service.update(category, request)

@router.delete('/{category_id}')
async def delete_category(
        category_id: UUID,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: CategoryService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    category = service.show(category_id)
    if not category:
        raise service.not_found_exception()
    return service.delete(category)
