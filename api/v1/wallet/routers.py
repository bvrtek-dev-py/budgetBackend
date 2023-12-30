from datetime import date
from typing import List, Annotated, Optional

from fastapi import APIRouter, Depends, Path, status

from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.transaction.requests import TransactionCreateRequest
from backend.api.v1.transaction.responses import TransactionBaseResponse
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
from backend.modules.transaction.dependencies import get_transaction_service
from backend.modules.transaction.services import TransactionService
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
):
    return await transaction_service.create(
        request.name,
        request.value,
        request.type,
        request.description,
        request.date,
        current_user.id,
        wallet_id,
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
    transactions_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
):
    wallet = await wallet_service.get_by_id(wallet_id)
    return await transactions_service.get_wallet_transactions(
        wallet, start_date, end_date
    )
