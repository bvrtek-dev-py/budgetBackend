from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.api.v1.auth.repsonses import TokenResponse
from backend.api.v1.common.responses import ErrorResponse
from backend.config.oauth2 import oauth2_scheme
from backend.dependencies.auth.creators import get_password_verify_service
from backend.dependencies.auth.permissions import (
    get_token_service,
)
from backend.dependencies.user.creators import get_user_service
from backend.modules.auth.exceptions import InvalidCredentials
from backend.modules.auth.schemas import TokenData
from backend.modules.auth.services import (
    PasswordVerifyService,
    TokenService,
)
from backend.modules.user.services import UserService

router = APIRouter(prefix="/api/v1/auth", tags=["APIv1 Auth"])


@router.post(
    "/login",
    responses={
        200: {"model": TokenResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: Annotated[UserService, Depends(get_user_service)],
    verify_service: Annotated[
        PasswordVerifyService, Depends(get_password_verify_service)
    ],
    token_service: Annotated[TokenService, Depends(get_token_service)],
):
    user = await user_service.get_by_username_or_email(form_data.username)

    if not verify_service.verify(form_data.password, user.password):
        raise InvalidCredentials()

    return {
        "token_type": "Bearer",
        "access_token": token_service.create_access_token(
            TokenData(user_id=user.id, sub=user.email)
        ),
        "refresh_token": token_service.create_refresh_token(
            TokenData(user_id=user.id, sub=user.email)
        ),
        "expired_at": token_service.get_expire_token_datetime(),
    }


@router.post(
    "/refresh-token",
    responses={
        200: {"model": TokenResponse},
        401: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
)
async def refresh_token(
    token: Annotated[str, Depends(oauth2_scheme)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
):
    decoded_data = token_service.decode(token)
    token_data = TokenData(user_id=decoded_data.id, sub=decoded_data.email)

    return {
        "token_type": "Bearer",
        "access_token": token_service.create_access_token(token_data),
        "refresh_token": token_service.create_refresh_token(token_data),
        "expired_at": token_service.get_expire_token_datetime(),
    }


@router.post("/logout")
async def logout():
    # TODO logout endpoint # pylint: disable=fixme
    ...
