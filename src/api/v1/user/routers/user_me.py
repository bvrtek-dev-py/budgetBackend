from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, status

from backend.src.api.v1.user.requests import UserUpdateRequest
from backend.src.api.v1.user.responses import UserBaseResponse
from backend.src.api.v1.category.responses import CategoryGetResponse
from backend.src.api.v1.common.responses import ErrorResponse
from backend.src.api.v1.subject.responses import SubjectBaseResponse
from backend.src.api.v1.wallet.responses import WalletGetResponse
from backend.src.dependencies.auth.permissions import get_current_user
from backend.src.dependencies.category.creators import get_category_service
from backend.src.dependencies.user.creators import get_user_service
from backend.src.core.modules.auth.schemas import CurrentUserDTO
from backend.src.core.modules.category.service import CategoryService
from backend.src.core.modules.transaction.enum import TransactionType
from backend.src.core.modules.user.service import UserService
from backend.src.core.modules.user.schemas import UserUpdateDTO

router = APIRouter(prefix="/api/v1/user/me", tags=["APIv1 User Me"])


@router.put(
    "/",
    responses={
        200: {"model": UserBaseResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    response_model=UserBaseResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user_me(
    current_user: Annotated[CurrentUserDTO, Depends(get_current_user)],
    request: UserUpdateRequest,
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return await user_service.update(
        current_user.id, UserUpdateDTO(**request.model_dump())
    )


@router.get(
    "/categories",
    responses={
        200: {"model": List[CategoryGetResponse]},
        401: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=List[CategoryGetResponse],
)
async def get_user_categories(
    current_user: Annotated[CurrentUserDTO, Depends(get_current_user)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
    transaction_type: Optional[TransactionType] = None,
):
    return await category_service.get_by_user_id(current_user.id, transaction_type)


@router.get(
    "/subjects",
    responses={
        200: {"model": List[SubjectBaseResponse]},
        401: {"model": ErrorResponse},
    },
    response_model=List[SubjectBaseResponse],
    status_code=status.HTTP_200_OK,
)
async def get_user_subjects(
    current_user: Annotated[CurrentUserDTO, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = await user_service.get_by_id(current_user.id)
    return user.subjects


@router.get(
    "/wallets",
    responses={
        200: {"model": List[WalletGetResponse]},
        401: {"model": ErrorResponse},
    },
    response_model=List[WalletGetResponse],
)
async def get_user_wallets(
    current_user: Annotated[CurrentUserDTO, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = await user_service.get_by_id(current_user.id)
    return user.wallets
