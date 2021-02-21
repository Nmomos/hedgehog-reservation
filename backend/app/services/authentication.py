from datetime import datetime, timedelta

import bcrypt
import jwt
from app.core.config import (ACCESS_TOKEN_EXPIRE_MINUTES, JWT_ALGORITHM,
                             JWT_AUDIENCE, JWT_TOKEN_PREFIX, SECRET_KEY)
from app.models.token import JWTCreds, JWTMeta, JWTPayload
from app.models.user import UserInDB, UserPasswordUpdate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthException(BaseException):
    pass


class AuthService:
    def create_salt_and_hashed_password(
            self, *, plaintext_password: str) -> UserPasswordUpdate:
        salt = self.generate_salt()
        hashed_password = self.hash_password(password=plaintext_password, salt=salt)

        return UserPasswordUpdate(salt=salt, password=hashed_password)

    def generate_salt(self) -> str:
        return bcrypt.gensalt().decode()

    def hash_password(self, *, password: str, salt: str) -> str:
        return pwd_context.hash(password + salt)

    def verify_password(self, *, password: str, salt: str, hashed_pw: str) -> bool:
        return pwd_context.verify(password + salt, hashed_pw)

    def create_access_token_for_user(
        self,
        *,
        user: UserInDB,
        secret_key: str = str(SECRET_KEY),
        audience: str = JWT_AUDIENCE,
        expires_in: int = ACCESS_TOKEN_EXPIRE_MINUTES,
    ) -> str:
        if not user or not isinstance(user, UserInDB):
            return None

        jwt_meta = JWTMeta(
            aud=audience,
            iat=datetime.timestamp(datetime.utcnow()),
            exp=datetime.timestamp(datetime.utcnow() + timedelta(minutes=expires_in)),
        )
        jwt_creds = JWTCreds(sub=user.email, username=user.username)
        token_payload = JWTPayload(**jwt_meta.dict(), **jwt_creds.dict(),)
        print(jwt.encode(
            token_payload.dict(),
            secret_key,
            algorithm=JWT_ALGORITHM
        ))
        access_token = jwt.encode(
            token_payload.dict(),
            secret_key,
            algorithm=JWT_ALGORITHM
        )

        return access_token
