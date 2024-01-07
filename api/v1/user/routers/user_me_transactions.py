from datetime import date, datetime
from typing import List, Annotated, Optional

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, status, Depends

from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.common.validators import validate_date_range
from backend.api.v1.transaction.responses.transaction import TransactionBaseResponse
from backend.api.v1.transaction.responses.transaction_statistics import (
    TransactionStatisticResponse,
    TransactionStatisticsResponse,
)
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.common.utils import get_first_day_of_month
from backend.modules.transaction.dependencies import (
    get_transaction_query_service,
    get_transaction_statistics_service,
)
from backend.modules.transaction.services.query_service import TransactionQueryService
from backend.modules.transaction.services.statistics_service import (
    TransactionStatisticsService,
)
from backend.modules.user.dependencies import get_user_service
from backend.modules.user.services import UserService

router = APIRouter(
    prefix="/api/v1/users/me/transactions", tags=["APIv1 User Me Transactions"]
)


@router.get(
    "/",
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
        current_user.id, get_first_day_of_month(datetime.now()) - relativedelta(years=1)
    )
