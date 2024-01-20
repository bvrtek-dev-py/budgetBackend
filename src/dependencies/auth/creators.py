from typing import Annotated

from fastapi import Depends
from passlib.context import CryptContext

from backend.src.config.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    REFRESH_TOKEN_SECRET_KEY,
)
from backend.src.core.modules.auth.services.password_services import (
    PasswordHashService,
    PasswordVerifyService,
)
from backend.src.core.modules.auth.services.token_service import TokenService


def get_crypt_context() -> CryptContext:
    return CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash_service(
    crypt_context: Annotated[CryptContext, Depends(get_crypt_context)]
) -> PasswordHashService:
    return PasswordHashService(crypt_context)


def get_password_verify_service(
    crypt_context: Annotated[CryptContext, Depends(get_crypt_context)]
) -> PasswordVerifyService:
    return PasswordVerifyService(crypt_context)


def get_token_service() -> TokenService:
    return TokenService(
        algorithm=ALGORITHM,
        secret_key=SECRET_KEY,
        refresh_token_secret_key=REFRESH_TOKEN_SECRET_KEY,
        token_expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )
