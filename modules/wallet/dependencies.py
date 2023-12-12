from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.setup import get_session
from backend.modules.wallet.repositories import WalletRepository
from backend.modules.wallet.services import WalletService


def get_wallet_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> WalletRepository:
    return WalletRepository(session)


def get_wallet_service(
    repository: Annotated[WalletRepository, Depends(get_wallet_repository)]
):
    return WalletService(repository)
