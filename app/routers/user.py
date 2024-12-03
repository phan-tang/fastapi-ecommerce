from fastapi import APIRouter, Request, Depends
from uuid import UUID
from typing import List

from models import UserViewModel, BaseUserViewModel, UserFormRequestModel
from services import UserService, AuthService, oa2_bearer

router = APIRouter(prefix="/users", tags=["User"])

@router.get('', response_model=List[UserViewModel])
async def get_users(
        request: Request,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: UserService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    return service.list(request)

@router.get('/{user_id}', response_model=UserViewModel | None)
async def get_user_by_id(
        user_id: UUID,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: UserService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    user = service.show(user_id)
    if not user:
        raise service.not_found_exception()
    return user

@router.post('', response_model=BaseUserViewModel)
async def create_user(
        request: UserFormRequestModel,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: UserService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    result = service.create(request)
    return result
    
@router.put('/{user_id}', response_model=BaseUserViewModel)
async def update_user(
        user_id: UUID,
        request: UserFormRequestModel,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: UserService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    user = service.show(user_id)
    return service.update(user, request)

@router.delete('/{user_id}')
async def delete_user(
        user_id: UUID,
        token: str = Depends(oa2_bearer),
        auth_service: AuthService = Depends(),
        service: UserService = Depends()):
    authenticated_user = auth_service.token_interceptor(token)
    if not service.check_admin_permission(authenticated_user):
        raise service.access_denied_exception()
    user = service.show(user_id)
    if not user:
        raise service.not_found_exception()
    return service.delete(user)
