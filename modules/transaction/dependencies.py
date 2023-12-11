from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from budgetBackend.database.setup import get_session
from budgetBackend.modules.transaction.repositories import TransactionRepository
from budgetBackend.modules.transaction.services import TransactionService


def get_transaction_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> TransactionRepository:
    return TransactionRepository(session)


def get_transaction_service(
    transaction_repository: Annotated[
        TransactionRepository, Depends(get_transaction_repository)
    ]
) -> TransactionService:
    return TransactionService(transaction_repository)
