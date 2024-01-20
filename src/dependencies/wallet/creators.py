from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.setup import get_session
from backend.src.core.modules.wallet.interfaces import WalletRepositoryInterface
from backend.src.core.modules.wallet.repositories import WalletRepository
from backend.src.core.modules.wallet.services import WalletService
from backend.src.core.modules.wallet.validators import WalletValidator


def get_wallet_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> WalletRepositoryInterface:
    return WalletRepository(session)


def get_wallet_service(
    repository: Annotated[WalletRepositoryInterface, Depends(get_wallet_repository)]
):
    return WalletService(repository)


def get_wallet_validator(
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)]
) -> WalletValidator:
    return WalletValidator(wallet_service)
