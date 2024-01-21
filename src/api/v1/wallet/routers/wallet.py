from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from backend.src.api.v1.common.responses import ErrorResponse
from backend.src.api.v1.wallet.requests import (
    WalletBaseRequest,
)
from backend.src.api.v1.wallet.responses import (
    WalletBaseResponse,
    WalletGetResponse,
)
from backend.src.core.modules.auth.schemas import CurrentUserDTO
from backend.src.core.modules.wallet.schemas import WalletPayloadDTO
from backend.src.core.modules.wallet.service import WalletService
from backend.src.dependencies.auth.permissions import get_current_user
from backend.src.dependencies.wallet.creators import (
    get_wallet_service,
)
from backend.src.dependencies.wallet.permissions import WalletOwnerPermission

router = APIRouter(prefix="/api/v1/wallets", tags=["APIv1 Wallet"])


@router.get(
    "/{wallet_id}",
    responses={
        200: {"model": WalletGetResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    response_model=WalletGetResponse,
    dependencies=[Depends(WalletOwnerPermission())],
)
async def get_wallet(
    wallet_id: Annotated[int, Path(gt=0)],
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
):
    return await wallet_service.get_by_id(wallet_id)


@router.post(
    "/",
    responses={
        201: {"model": WalletBaseResponse},
        401: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    response_model=WalletBaseResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_wallet(
    request: WalletBaseRequest,
    current_user: Annotated[CurrentUserDTO, Depends(get_current_user)],
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
):
    return await wallet_service.create(
        current_user.id, WalletPayloadDTO(**request.model_dump())
    )


@router.put(
    "/{wallet_id}",
    responses={
        200: {"model": WalletBaseResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        409: {"model": ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=WalletBaseResponse,
    dependencies=[Depends(WalletOwnerPermission())],
)
async def update_wallet(
    wallet_id: Annotated[int, Path(gt=0)],
    request: WalletBaseRequest,
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
):
    return await wallet_service.update(
        wallet_id, WalletPayloadDTO(**request.model_dump())
    )


@router.delete(
    "/{wallet_id}",
    responses={
        204: {},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
    },
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(WalletOwnerPermission())],
)
async def delete_wallet(
    wallet_id: Annotated[int, Path(gt=0)],
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
):
    return await wallet_service.delete(wallet_id)
