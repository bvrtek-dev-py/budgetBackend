from datetime import datetime
from typing import Annotated, List

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, Path
from starlette import status

from backend.src.api.v1.common.query_parameters import DateRangeParameters
from backend.src.api.v1.common.responses import ErrorResponse
from backend.src.api.v1.transaction.requests.transaction import TransactionCreateRequest
from backend.src.api.v1.transaction.responses.transaction import TransactionBaseResponse
from backend.src.api.v1.transaction.responses.transaction_statistics import (
    WalletTransactionStatisticsResponse,
    WalletTransactionStatisticResponse,
)
from backend.src.core.modules.auth.schemas import CurrentUserDTO
from backend.src.core.modules.common.utils import get_first_day_of_month
from backend.src.core.modules.transaction.schemas.transaction import (
    TransactionCreateDTO,
)
from backend.src.core.modules.transaction.services.crud_service import (
    TransactionService,
)
from backend.src.core.modules.transaction.services.query_service import (
    TransactionQueryService,
)
from backend.src.core.modules.transaction.services.statistics_service import (
    TransactionStatisticsService,
)
from backend.src.dependencies.auth.permissions import get_current_user
from backend.src.dependencies.category.permissions import CategoryOwnerPermission
from backend.src.dependencies.common.enums import IdentifierSource
from backend.src.dependencies.subject.permissions import SubjectOwnerPermission
from backend.src.dependencies.transaction.creators import (
    get_transaction_service,
    get_transaction_query_service,
    get_transaction_statistics_service,
)
from backend.src.dependencies.wallet.permissions import WalletOwnerPermission

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
        Depends(WalletOwnerPermission()),
        Depends(SubjectOwnerPermission(source=IdentifierSource.REQUEST_BODY)),
        Depends(CategoryOwnerPermission(source=IdentifierSource.REQUEST_BODY)),
    ],
)
async def create_wallet_transaction(
    wallet_id: Annotated[int, Path(gt=0)],
    request: TransactionCreateRequest,
    current_user: Annotated[CurrentUserDTO, Depends(get_current_user)],
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
    dependencies=[Depends(WalletOwnerPermission())],
)
async def get_wallet_transactions(
    wallet_id: Annotated[int, Path(gt=0)],
    transaction_query_service: Annotated[
        TransactionQueryService, Depends(get_transaction_query_service)
    ],
    date_range: Annotated[DateRangeParameters, Depends()],
):
    return await transaction_query_service.get_wallet_transactions(
        wallet_id, date_range.start_date, date_range.end_date
    )


@router.get(
    "/statistics",
    responses={
        200: {"model": WalletTransactionStatisticsResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    response_model=WalletTransactionStatisticsResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(WalletOwnerPermission())],
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
        200: {"model": WalletTransactionStatisticResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    response_model=WalletTransactionStatisticResponse,
    dependencies=[Depends(WalletOwnerPermission())],
)
async def get_wallet_balance(
    wallet_id: Annotated[int, Path(gt=0)],
    transaction_statistics_service: Annotated[
        TransactionStatisticsService, Depends(get_transaction_statistics_service)
    ],
):
    return await transaction_statistics_service.get_wallet_balance(wallet_id)
