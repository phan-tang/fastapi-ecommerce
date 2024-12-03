from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from jose import jwt, JWTError
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from config import JWT_ALGORITHM, JWT_SECRET

from schemas import User
from repositories import UserRepository
from .base import BaseService
from .base_auth import BaseAuthService

oa2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

class AuthService(BaseService, BaseAuthService):
    repository: UserRepository

    def __init__(self, repository: UserRepository = Depends()) -> None:
        self.repository = repository

    def authenticate_user(self, username: str, password: str, db: Session):
        user = self.repository.find_element_by_key('username', username)
        if not user:
            return False
        if not self.verify_password(password, user.password):
            return False
        return user

    def create_access_token(self, user: User, expire_minutes: int = 10):
        expire_time = datetime.utcnow() + timedelta(minutes=expire_minutes)
        claims = {
            "sub": user.username,
            "id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_type": user.user_type.value,
            "exp": expire_time,
            'minutes': expire_minutes
        }
        return jwt.encode(claims=claims, key=JWT_SECRET, algorithm=JWT_ALGORITHM)

    def token_interceptor(self, token: str) -> User:
        try:
            payload = jwt.decode(token=token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
            if payload.get("id") is None:
                raise self.token_exception()
            user = User()
            user.username = payload.get("sub")
            user.id = payload.get("id")
            user.company_id = payload.get("company_id")
            user.first_name = payload.get("first_name")
            user.last_name = payload.get("last_name")
            user.user_type = payload.get("user_type")
            return user
        except JWTError:
            raise self.access_denied_exception()

