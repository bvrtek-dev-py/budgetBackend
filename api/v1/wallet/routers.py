from datetime import date, datetime
from typing import List, Annotated, Optional

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Depends, Path, status

from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.common.validators import validate_date_range
from backend.api.v1.transaction.requests import TransactionCreateRequest
from backend.api.v1.transaction.responses.transaction import TransactionBaseResponse
from backend.api.v1.transaction.responses.transaction_statistics import (
    TransactionStatisticsResponse,
    TransactionStatisticResponse,
)
from backend.api.v1.wallet.requests import (
    WalletUpdateRequest,
    WalletCreateRequest,
)
from backend.api.v1.wallet.responses import (
    WalletBaseResponse,
    WalletGetResponse,
)
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.common.exceptions import PermissionDenied
from backend.modules.common.utils import get_first_day_of_month
from backend.modules.subject.dependencies import get_subject_validator
from backend.modules.subject.validators import SubjectValidator
from backend.modules.transaction.dependencies import (
    get_transaction_service,
    get_transaction_query_service,
    get_transaction_statistics_service,
)
from backend.modules.transaction.services.crud_service import TransactionService
from backend.modules.transaction.services.query_service import TransactionQueryService
from backend.modules.transaction.services.statistics_service import (
    TransactionStatisticsService,
)
from backend.modules.wallet.dependencies import (
    get_wallet_service,
    wallet_owner_permission,
)
from backend.modules.wallet.services import WalletService

router = APIRouter(prefix="/api/v1/wallets", tags=["APIv1 Wallet"])


@router.get(
    "/{wallet_id}",
    responses={200: {"model": WalletGetResponse}, 404: {"model": ErrorResponse}},
    response_model=WalletGetResponse,
    dependencies=[Depends(wallet_owner_permission)],
)
async def get_wallet(
    wallet_id: Annotated[int, Path(gt=0)],
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
):
    return await wallet_service.get_by_id(wallet_id)


@router.post(
    "/",
    responses={201: {"model": WalletBaseResponse}},
    response_model=WalletBaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_wallet(
    request: WalletCreateRequest,
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
):
    return await wallet_service.create(
        current_user.id, request.name, request.description
    )


@router.put(
    "/{wallet_id}",
    responses={200: {"model": WalletBaseResponse}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_200_OK,
    response_model=WalletBaseResponse,
    dependencies=[Depends(wallet_owner_permission)],
)
async def update_wallet(
    wallet_id: Annotated[int, Path(gt=0)],
    request: WalletUpdateRequest,
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
):
    return await wallet_service.update(wallet_id, request.name, request.description)


@router.delete(
    "/{wallet_id}",
    responses={204: {}, 404: {"model": ErrorResponse}},
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(wallet_owner_permission)],
)
async def delete_wallet(
    wallet_id: Annotated[int, Path(gt=0)],
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
):
    return await wallet_service.delete(wallet_id)


@router.post(
    "/{wallet_id}/transactions",
    responses={201: {"model": TransactionBaseResponse}, 422: {"model": ErrorResponse}},
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(wallet_owner_permission)],
)
async def create_wallet_transaction(
    wallet_id: Annotated[int, Path(gt=0)],
    request: TransactionCreateRequest,
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
    subject_validator: Annotated[SubjectValidator, Depends(get_subject_validator)],
):
    if (
        await subject_validator.user_is_subject_owner(
            current_user.id, request.subject_id
        )
        is False
    ):
        raise PermissionDenied()

    return await transaction_service.create(
        request.name,
        request.value,
        request.type,
        request.description,
        request.date,
        current_user.id,
        wallet_id,
        request.subject_id,
    )


@router.get(
    "/{wallet_id}/transactions",
    responses={200: {"model": List[TransactionBaseResponse]}},
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
    "/{wallet_id}/statistics",
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
    "/{wallet_id}/balance",
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
