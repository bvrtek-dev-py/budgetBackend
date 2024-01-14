from datetime import date, datetime
from typing import Annotated, List, Optional

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, Path
from starlette import status

from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.common.validators import validate_date_range
from backend.api.v1.transaction.requests import TransactionCreateRequest
from backend.api.v1.transaction.responses.transaction import TransactionBaseResponse
from backend.api.v1.transaction.responses.transaction_statistics import (
    TransactionStatisticsResponse,
    TransactionStatisticResponse,
)
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.category.dependencies import category_owner_permission
from backend.modules.common.utils import get_first_day_of_month
from backend.modules.subject.dependencies import (
    subject_owner_permission,
)
from backend.modules.transaction.dependencies import (
    get_transaction_service,
    get_transaction_query_service,
    get_transaction_statistics_service,
)
from backend.modules.transaction.schemas import TransactionCreateDTO
from backend.modules.transaction.services.crud_service import TransactionService
from backend.modules.transaction.services.query_service import TransactionQueryService
from backend.modules.transaction.services.statistics_service import (
    TransactionStatisticsService,
)
from backend.modules.wallet.dependencies import (
    wallet_owner_permission,
    get_wallet_service,
)
from backend.modules.wallet.services import WalletService

router = APIRouter(
    prefix="/api/v1/wallets/{wallet_id}/transactions",
    tags=["APIv1 Wallet Transactions"],
)


@router.post(
    "/",
    responses={
        201: {"model": TransactionBaseResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(wallet_owner_permission),
        Depends(subject_owner_permission),
        Depends(category_owner_permission),
    ],
)
async def create_wallet_transaction(
    wallet_id: Annotated[int, Path(gt=0)],
    request: TransactionCreateRequest,
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
):
    return await transaction_service.create(
        wallet_id, current_user.id, TransactionCreateDTO(**request.model_dump())
    )


@router.get(
    "/",
    responses={
        200: {"model": List[TransactionBaseResponse]},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },
    response_model=List[TransactionBaseResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(wallet_owner_permission)],
)
async def get_wallet_transactions(
    wallet_id: Annotated[int, Path(gt=0)],
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
    transaction_query_service: Annotated[
        TransactionQueryService, Depends(get_transaction_query_service)
    ],
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    if start_date is not None and end_date is not None:
        validate_date_range(start_date, end_date)

    wallet = await wallet_service.get_by_id(wallet_id)

    return await transaction_query_service.get_wallet_transactions(
        wallet, start_date, end_date
    )


@router.get(
    "/statistics",
    responses={
        200: {"model": TransactionStatisticsResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    response_model=TransactionStatisticsResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(wallet_owner_permission)],
)
async def get_wallet_statistics(
    wallet_id: Annotated[int, Path(gt=0)],
    statistics_service: Annotated[
        TransactionStatisticsService, Depends(get_transaction_statistics_service)
    ],
):
    return await statistics_service.get_statistics_for_wallet(
        wallet_id, get_first_day_of_month(datetime.now()) - relativedelta(years=1)
    )


@router.get(
    "/balance",
    responses={
        200: {"model": TransactionStatisticResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    response_model=TransactionStatisticResponse,
    dependencies=[Depends(wallet_owner_permission)],
)
async def get_wallet_balance(
    wallet_id: Annotated[int, Path(gt=0)],
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
    transaction_statistics_service: Annotated[
        TransactionStatisticsService, Depends(get_transaction_statistics_service)
    ],
):
    wallet = await wallet_service.get_by_id(wallet_id)
    return await transaction_statistics_service.get_wallet_balance(wallet)
