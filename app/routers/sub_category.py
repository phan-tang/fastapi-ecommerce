from fastapi import APIRouter, Request, Depends
from uuid import UUID
from typing import List

from models import SubCategoryFormRequestModel, SubCategoryViewModel, BaseSubCategoryViewModel
from services import SubCategoryService, AuthService, oa2_bearer

import time

router = APIRouter(prefix="/sub_categories", tags=["SubCategory"])

@router.get('', response_model=List[SubCategoryViewModel])
async def get_sub_categories(
        request: Request,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: SubCategoryService = Depends()):
    start_time = time.time()
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    result = service.list(request)
    print(f"Execution time: {time.time()-start_time}")
    return result

@router.get('/{sub_category_id}', response_model=SubCategoryViewModel | None)
async def get_sub_category_by_id(
        sub_category_id: UUID,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: SubCategoryService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    sub_category = service.show(sub_category_id)
    if not sub_category:
        raise service.not_found_exception()
    return sub_category

@router.post('', response_model=BaseSubCategoryViewModel)
async def create_sub_category(
        request: SubCategoryFormRequestModel,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: SubCategoryService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    result = service.create(request)
    return result

@router.put('/{sub_category_id}', response_model=BaseSubCategoryViewModel)
async def update_sub_category(
        sub_category_id: UUID,
        request: SubCategoryFormRequestModel,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: SubCategoryService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    sub_category = service.show(sub_category_id)
    return service.update(sub_category, request)

@router.delete('/{sub_category_id}')
async def delete_sub_category(
        sub_category_id: UUID,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: SubCategoryService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    sub_category = service.show(sub_category_id)
    if not sub_category:
        raise service.not_found_exception()
    return service.delete(sub_category)
