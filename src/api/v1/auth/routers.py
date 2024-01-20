from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.src.api.v1.auth.requests import PasswordChangeRequest
from backend.src.api.v1.user.responses import UserBaseResponse
from backend.src.api.v1.auth.repsonses import TokenResponse
from backend.src.api.v1.common.responses import ErrorResponse
from backend.src.config.oauth2 import oauth2_scheme
from backend.src.dependencies.auth.creators import (
    get_password_verify_service,
    get_token_service,
)
from backend.src.dependencies.user.creators import get_user_service
from backend.src.core.modules.auth.exceptions import InvalidCredentials
from backend.src.core.modules.auth.schemas import (
    TokenData,
    CurrentUserData,
    ChangePasswordDTO,
)
from backend.src.core.modules.user.services import UserService
from backend.src.dependencies.auth.permissions import get_current_user
from backend.src.core.modules.auth.services.password_services import (
    PasswordChangeService,
    PasswordVerifyService,
)
from backend.src.dependencies.auth.password_changer import get_password_change_service
from backend.src.core.modules.auth.services.token_service import TokenService

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


@router.post(
    "/change-password",
    responses={
        200: {"model": UserBaseResponse},
        401: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    response_model=UserBaseResponse,
    status_code=status.HTTP_200_OK,
)
async def change_password(
    request: PasswordChangeRequest,
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    password_change_service: Annotated[
        PasswordChangeService, Depends(get_password_change_service)
    ],
):
    return await password_change_service.change_password(
        current_user.id, ChangePasswordDTO(**request.model_dump())
    )
