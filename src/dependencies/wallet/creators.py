from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.setup import get_session
from backend.src.core.modules.wallet.repository_interface import (
    WalletRepositoryInterface,
)
from backend.src.core.modules.wallet.repository import WalletRepository
from backend.src.core.modules.wallet.service import WalletService
from backend.src.core.modules.wallet.validator import WalletValidator
from backend.src.core.modules.wallet.use_case import WalletRetrievalUseCase


def get_wallet_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> WalletRepositoryInterface:
    return WalletRepository(session)


def get_wallet_retrieval_use_case(
    repository: Annotated[WalletRepositoryInterface, Depends(get_wallet_repository)]
) -> WalletRetrievalUseCase:
    return WalletRetrievalUseCase(repository)


def get_wallet_service(
    repository: Annotated[WalletRepositoryInterface, Depends(get_wallet_repository)],
    retrieval_use_case: Annotated[
        WalletRetrievalUseCase, Depends(get_wallet_retrieval_use_case)
    ],
) -> WalletService:
    return WalletService(repository=repository, retrieval_use_case=retrieval_use_case)


def get_wallet_validator(
    retrieval_use_case: Annotated[
        WalletRetrievalUseCase, Depends(get_wallet_retrieval_use_case)
    ]
) -> WalletValidator:
    return WalletValidator(retrieval_use_case)
