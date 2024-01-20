from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.src.api.v1.auth.repsonses import TokenResponse
from backend.src.api.v1.auth.requests import PasswordChangeRequest
from backend.src.api.v1.common.responses import ErrorResponse
from backend.src.api.v1.user.responses import UserBaseResponse
from backend.src.config.oauth2 import oauth2_scheme
from backend.src.core.modules.auth.schemas import (
    AuthenticatedUserDTO,
    CurrentUserData,
    ChangePasswordDTO,
)
from backend.src.core.modules.auth.services.login_service import LoginService
from backend.src.core.modules.auth.services.password_services import (
    PasswordChangeService,
)
from backend.src.core.modules.auth.services.token_service import TokenService
from backend.src.dependencies.auth.creators import (
    get_token_service,
)
from backend.src.dependencies.auth.providers import (
    get_password_change_service,
    get_login_service,
)
from backend.src.dependencies.auth.permissions import get_current_user

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
    login_service: Annotated[LoginService, Depends(get_login_service)],
):
    return await login_service.login(form_data.username, form_data.password)


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
    token_data = AuthenticatedUserDTO(id=decoded_data.id, sub=decoded_data.email)

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
