from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.setup import get_session
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.common.exceptions import PermissionDenied
from backend.modules.transaction.repositories import TransactionRepository
from backend.modules.transaction.services.crud_service import TransactionService
from backend.modules.transaction.services.query_service import TransactionQueryService
from backend.modules.transaction.services.statistics_service import (
    TransactionStatisticsService,
)


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


def _get_transaction_id(transaction_id: int = Path(...)) -> int:
    return transaction_id


async def transaction_owner_permission(
    transaction_id: Annotated[int, Depends(_get_transaction_id)],
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    transaction_service: Annotated[
        TransactionService, Depends(get_transaction_service)
    ],
):
    category = await transaction_service.get_by_id(transaction_id)

    if category.user_id != current_user.id:
        raise PermissionDenied()
