from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext

from backend.config.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    REFRESH_TOKEN_SECRET_KEY,
)
from backend.config.oauth2 import oauth2_scheme
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.auth.services import (
    PasswordHashService,
    TokenService,
    PasswordVerifyService,
)


def _get_crypt_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash_service(
    crypt_context: Annotated[CryptContext, Depends(_get_crypt_context)]
) -> PasswordHashService:
    return PasswordHashService(crypt_context)


def get_password_verify_service(
    crypt_context: Annotated[CryptContext, Depends(_get_crypt_context)]
) -> PasswordVerifyService:
    return PasswordVerifyService(crypt_context)


def get_token_service() -> TokenService:
    return TokenService(
        algorithm=ALGORITHM,
        secret_key=SECRET_KEY,
        refresh_token_secret_key=REFRESH_TOKEN_SECRET_KEY,
        token_expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
) -> CurrentUserData:
    return token_service.decode(token)
