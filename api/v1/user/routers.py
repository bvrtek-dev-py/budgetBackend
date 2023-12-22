from typing import Annotated, List

from fastapi import APIRouter, Depends, Path
from fastapi import status

from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.transaction.responses import TransactionBaseResponse
from backend.api.v1.user.requests import UserCreateRequest, UserUpdateRequest
from backend.api.v1.user.responses import UserBaseResponse
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.user.dependencies import get_user_service
from backend.modules.user.services import UserService

router = APIRouter(prefix="/api/v1/users", tags=["APIv1 User"])


@router.post(
    "/",
    responses={
        201: {"model": UserBaseResponse},
        409: {"model": ErrorResponse},
        422: {"model": ErrorResponse},
    },
    response_model=UserBaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: UserCreateRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.create(
        request.username,
        request.email,
        request.first_name,
        request.last_name,
        request.password1,
        request.password2,
    )


@router.put(
    "/{user_id}",
    responses={
        200: {"model": UserBaseResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    response_model=UserBaseResponse,
)
async def update_user(
    user_id: Annotated[int, Path(gt=0)],
    request: UserUpdateRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.update(
        user_id, request.username, request.first_name, request.last_name
    )


@router.get(
    "/{user_id}",
    responses={
        200: {"model": UserBaseResponse},
        404: {"model": ErrorResponse},
    },
    response_model=UserBaseResponse,
)
async def get_user(
    user_id: int, user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.get_by_id(user_id)


@router.get("/", response_model=List[UserBaseResponse], status_code=status.HTTP_200_OK)
async def get_users(user_service: Annotated[UserService, Depends(get_user_service)]):
    return await user_service.get_all()


@router.delete(
    "/{user_id}",
    responses={
        204: {},
        404: {"model": ErrorResponse},
    },
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    user_id: int, user_service: Annotated[UserService, Depends(get_user_service)]
):
    return await user_service.delete(user_id)


@router.get(
    "/me/transactions",
    responses={
        200: {"model": List[TransactionBaseResponse]},
        401: {"model": ErrorResponse},
    },
    response_model=List[TransactionBaseResponse],
    status_code=status.HTTP_200_OK,
)
async def get_user_transactions(
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = await user_service.get_by_id(current_user.id)
    return user.transactions
