from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from backend.api.v1.auth.repsonses import TokenResponse
from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.user.responses import UserBaseResponse
from backend.config.oauth2 import oauth2_scheme
from backend.modules.auth.dependencies import (
    get_password_verify_service,
    get_token_service,
    get_current_user,
)
from backend.modules.auth.exceptions import InvalidCredentials
from backend.modules.auth.services import (
    PasswordVerifyService,
    TokenService,
)
from backend.modules.user.dependencies import get_user_service
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
        raise InvalidCredentials

    return {
        "token_type": "Bearer",
        "access_token": token_service.create_access_token({"sub": user.email}),
        "refresh_token": token_service.create_refresh_token({"sub": user.email}),
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
    email = token_service.decode(token)["email"]

    return {
        "token_type": "Bearer",
        "access_token": token_service.create_access_token({"sub": email}),
        "refresh_token": token_service.create_refresh_token({"sub": email}),
        "expired_at": token_service.get_expire_token_datetime(),
    }


@router.post("/logout")
async def logout():
    # TODO logout endpoint # pylint: disable=fixme
    ...


@router.get("/user-me", response_model=UserBaseResponse)
async def user_me(
    email: Annotated[str, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.get_by_email(email)
