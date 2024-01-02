from typing import Annotated

from fastapi import Depends
from fastapi.params import Path
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.setup import get_session
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.common.exceptions import PermissionDenied
from backend.modules.wallet.interfaces import WalletRepositoryInterface
from backend.modules.wallet.repositories import WalletRepository
from backend.modules.wallet.services import WalletService


def get_wallet_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> WalletRepositoryInterface:
    return WalletRepository(session)


def get_wallet_service(
    repository: Annotated[WalletRepositoryInterface, Depends(get_wallet_repository)]
):
    return WalletService(repository)


def get_wallet_id(wallet_id: int = Path(...)) -> int:  # type: ignore
    return wallet_id


async def wallet_owner_permission(
    wallet_id: Annotated[int, Depends(get_wallet_id)],
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)],
):
    wallet = await wallet_service.get_by_id(wallet_id)

    if wallet.user_id != current_user.id:
        raise PermissionDenied()
