from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from backend.api.v1.common.responses import ErrorResponse
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
