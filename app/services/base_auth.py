from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class BaseAuthService:
    def verify_password(self, plain_password: str, hashed_password: str):
        return bcrypt_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return bcrypt_context.hash(password)