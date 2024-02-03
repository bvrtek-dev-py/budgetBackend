from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.setup import get_session
from backend.src.core.modules.transaction.repository_interface import (
    TransactionRepositoryInterface,
)
from backend.src.core.modules.transaction.repository import TransactionRepository
from backend.src.core.modules.transaction.services.crud_service import (
    TransactionService,
)
from backend.src.core.modules.transaction.services.query_service import (
    TransactionQueryService,
)
from backend.src.core.modules.transaction.services.statistics_service import (
    TransactionStatisticsService,
)
from backend.src.core.modules.transaction.services.transfer_service import (
    TransactionTransferService,
)
from backend.src.core.modules.transaction.validator import TransactionValidator
from backend.src.core.modules.transaction.use_case import TransactionRetrievalUseCase


def get_transaction_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> TransactionRepositoryInterface:
    return TransactionRepository(session)


def get_transaction_retrieval_use_case(
    repository: Annotated[TransactionRepository, Depends(get_transaction_repository)]
) -> TransactionRetrievalUseCase:
    return TransactionRetrievalUseCase(repository)


def get_transaction_service(
    repository: Annotated[TransactionRepository, Depends(get_transaction_repository)],
    retrieval_use_case: Annotated[
        TransactionRetrievalUseCase, Depends(get_transaction_retrieval_use_case)
    ],
) -> TransactionService:
    return TransactionService(
        repository=repository, retrieval_use_case=retrieval_use_case
    )


def get_transaction_query_service(
    repository: Annotated[TransactionRepository, Depends(get_transaction_repository)]
) -> TransactionQueryService:
    return TransactionQueryService(repository)


def get_transaction_statistics_service(
    repository: Annotated[TransactionRepository, Depends(get_transaction_repository)]
) -> TransactionStatisticsService:
    return TransactionStatisticsService(repository)


def get_transaction_transfer_service(
    repository: Annotated[TransactionRepository, Depends(get_transaction_repository)]
) -> TransactionTransferService:
    return TransactionTransferService(repository)


def get_transaction_validator(
    retrieval_use_case: Annotated[
        TransactionRetrievalUseCase, Depends(get_transaction_retrieval_use_case)
    ]
) -> TransactionValidator:
    return TransactionValidator(retrieval_use_case)
