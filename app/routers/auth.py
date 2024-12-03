from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database import get_db_session

from services import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post('/token')
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()
        , service: AuthService = Depends()
        , db: Session = Depends(get_db_session)):
    user = service.authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise service.token_exception()
    token = service.create_access_token(user, 30)
    return {
        "access_token": token,
        "token_type": "bearer"
    }