from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from budgetBackend.database.setup import get_session
from budgetBackend.modules.wallet.repositories import WalletRepository
from budgetBackend.modules.wallet.services import WalletService


def get_wallet_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> WalletRepository:
    return WalletRepository(session)


def get_wallet_service(
    repository: Annotated[WalletRepository, Depends(get_wallet_repository)]
):
    return WalletService(repository)
