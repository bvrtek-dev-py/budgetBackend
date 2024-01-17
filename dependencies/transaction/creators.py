from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.setup import get_session
from backend.modules.transaction.interfaces import TransactionRepositoryInterface
from backend.modules.transaction.repositories import TransactionRepository
from backend.modules.transaction.services.crud_service import TransactionService
from backend.modules.transaction.services.query_service import TransactionQueryService
from backend.modules.transaction.services.statistics_service import (
    TransactionStatisticsService,
)
from backend.modules.transaction.services.transfer_service import (
    TransactionTransferService,
)
from backend.modules.transaction.validators import TransactionValidator


def get_transaction_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> TransactionRepositoryInterface:
    return TransactionRepository(session)


def get_transaction_service(
    transaction_repository: Annotated[
        TransactionRepository, Depends(get_transaction_repository)
    ]
) -> TransactionService:
    return TransactionService(transaction_repository)


def get_transaction_query_service(
    transaction_repository: Annotated[
        TransactionRepository, Depends(get_transaction_repository)
    ]
) -> TransactionQueryService:
    return TransactionQueryService(transaction_repository)


def get_transaction_statistics_service(
    transaction_repository: Annotated[
        TransactionRepository, Depends(get_transaction_repository)
    ]
) -> TransactionStatisticsService:
    return TransactionStatisticsService(transaction_repository)


def get_transaction_transfer_service(
    transaction_repository: Annotated[
        TransactionRepository, Depends(get_transaction_repository)
    ]
) -> TransactionTransferService:
    return TransactionTransferService(transaction_repository)


def get_transaction_validator(
    transaction_service: Annotated[TransactionService, Depends(get_transaction_service)]
) -> TransactionValidator:
    return TransactionValidator(transaction_service)
