from typing import List, Annotated

from fastapi import APIRouter, Depends, Path

from budgetBackend.api.v1.common.responses import ErrorResponse
from budgetBackend.api.v1.wallet.requests import (
    WalletUpdateRequest,
    WalletCreateRequest,
)
from budgetBackend.api.v1.wallet.responses import WalletBaseResponse
from budgetBackend.modules.wallet.dependencies import get_wallet_service
from budgetBackend.modules.wallet.services import WalletService

router = APIRouter(prefix="/api/v1/wallets", tags=["APIv1 Wallet"])


@router.get("/", response_model=List[WalletBaseResponse])
async def get_wallets(
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)]
):
    return await wallet_service.get_all()


@router.get(
    "/{wallet_id}",
    responses={200: {"model": WalletBaseResponse}, 404: {"model": ErrorResponse}},
)
async def get_wallet(
    wallet_id: Annotated[int, Path(gt=0)],
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
):
    return await wallet_service.get_by_id(wallet_id)


@router.post("/", responses={201: {"model": WalletBaseResponse}})
async def create_wallet(
    request: WalletCreateRequest,
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
):
    return await wallet_service.create(request.name, request.description)


@router.put(
    "/{wallet_id}",
    responses={200: {"model": WalletBaseResponse}, 404: {"model": ErrorResponse}},
)
async def update_wallet(
    wallet_id: Annotated[int, Path(gt=0)],
    request: WalletUpdateRequest,
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
):
    return await wallet_service.update(wallet_id, request.name, request.description)


@router.delete(
    "/{wallet_id}",
    responses={200: {"model": WalletBaseResponse}, 404: {"model": ErrorResponse}},
)
async def delete_wallet(
    wallet_id: Annotated[int, Path(gt=0)],
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
):
    return await wallet_service.delete(wallet_id)
