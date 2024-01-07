from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, status

from backend.api.v1.category.responses import CategoryGetResponse
from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.subject.responses import SubjectBaseResponse
from backend.api.v1.wallet.responses import WalletGetResponse
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.category.dependencies import get_category_service
from backend.modules.category.services import CategoryService
from backend.modules.transaction.enums import TransactionType
from backend.modules.user.dependencies import get_user_service
from backend.modules.user.services import UserService

router = APIRouter(prefix="/api/v1/users/me", tags=["APIv1 User Me"])


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
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
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
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
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
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = await user_service.get_by_id(current_user.id)
    return user.wallets
