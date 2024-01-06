from datetime import date, datetime
from typing import Annotated, List, Optional

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends
from starlette import status

from backend.api.v1.category.responses import CategoryGetResponse
from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.common.validators import validate_date_range
from backend.api.v1.subject.responses import SubjectBaseResponse
from backend.api.v1.transaction.responses.transaction import TransactionBaseResponse
from backend.api.v1.transaction.responses.transaction_statistics import (
    TransactionStatisticsResponse,
    TransactionStatisticResponse,
)
from backend.api.v1.wallet.responses import WalletGetResponse
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.category.dependencies import get_category_service
from backend.modules.category.services import CategoryService
from backend.modules.transaction.dependencies import (
    get_transaction_statistics_service,
    get_transaction_query_service,
)
from backend.modules.transaction.enums import TransactionType
from backend.modules.transaction.services.query_service import TransactionQueryService
from backend.modules.transaction.services.statistics_service import (
    TransactionStatisticsService,
)
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
    # Look for different solution (using relationship)
    return await category_service.get_by_user_id(current_user.id, transaction_type)


@router.get(
    "/transactions",
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
    transaction_query_service: Annotated[
        TransactionQueryService, Depends(get_transaction_query_service)
    ],
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    if start_date is not None and end_date is not None:
        validate_date_range(start_date, end_date)

    user = await user_service.get_by_id(current_user.id)
    return await transaction_query_service.get_user_transactions(
        user, start_date, end_date
    )


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
    responses={200: {"model": List[WalletGetResponse]}},
    response_model=List[WalletGetResponse],
)
async def get_user_wallets(
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user = await user_service.get_by_id(current_user.id)
    return user.wallets


@router.get(
    "/balance",
    responses={
        200: {"model": TransactionStatisticResponse},
        401: {"model": ErrorResponse},
    },
    response_model=TransactionStatisticResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_balance(
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    transaction_statistics_service: Annotated[
        TransactionStatisticsService, Depends(get_transaction_statistics_service)
    ],
):
    return await transaction_statistics_service.get_user_balance(current_user.id)


@router.get(
    "/statistics",
    responses={
        200: {"model": TransactionStatisticsResponse},
        401: {"model": ErrorResponse},
    },
    response_model=TransactionStatisticsResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_statistics(
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    transaction_statistics_service: Annotated[
        TransactionStatisticsService, Depends(get_transaction_statistics_service)
    ],
):
    return await transaction_statistics_service.get_statistics_for_user(
        current_user.id, datetime.now().replace(day=1) - relativedelta(years=1)
    )
