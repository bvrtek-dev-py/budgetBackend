from typing import Annotated

from fastapi import Depends, Path, APIRouter
from starlette import status

from backend.api.v1.common.responses import ErrorResponse
from backend.api.v1.transaction.requests.transaction_transfer import (
    TransactionTransferRequest,
)
from backend.api.v1.transaction.responses.transaction_transfer import (
    TransactionTransferResponse,
)
from backend.dependencies.auth.permissions import get_current_user
from backend.dependencies.transaction.creators import get_transaction_transfer_service
from backend.dependencies.wallet.permissions import WalletOwnerPermission
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.transaction.schemas.transaction import TransactionTransferDTO
from backend.modules.transaction.services.transfer_service import (
    TransactionTransferService,
)

router = APIRouter(
    prefix="/api/v1/wallets/{sender_id}/wallets/{receiver_id}/transfer",
    tags=["APIv1 Wallet Transactions"],
)


@router.post(
    "/",
    responses={
        201: {"model": TransactionTransferResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
    },
    status_code=status.HTTP_201_CREATED,
    dependencies=[
        Depends(WalletOwnerPermission(name="sender_id")),
        Depends(WalletOwnerPermission(name="receiver_id")),
    ],
)
async def transfer_transaction(
    sender_id: Annotated[int, Path(gt=0)],
    receiver_id: Annotated[int, Path(gt=0)],
    request: TransactionTransferRequest,
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    transfer_service: Annotated[
        TransactionTransferService, Depends(get_transaction_transfer_service)
    ],
):
    return await transfer_service.transfer(
        sender_id,
        receiver_id,
        current_user.id,
        TransactionTransferDTO(**request.model_dump()),
    )
