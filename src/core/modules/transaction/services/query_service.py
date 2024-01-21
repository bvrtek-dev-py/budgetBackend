from datetime import date
from typing import Optional, Sequence

from backend.src.core.modules.transaction.model import Transaction
from backend.src.core.modules.transaction.repository import TransactionRepository


class TransactionQueryService:
    def __init__(self, repository: TransactionRepository):
        self._repository = repository

    async def get_user_transactions(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Sequence[Transaction]:
        return await self._repository.get_by_user_id(user_id, start_date, end_date)

    async def get_wallet_transactions(
        self,
        wallet_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Sequence[Transaction]:
        return await self._repository.get_by_wallet_id(wallet_id, start_date, end_date)

    async def get_subject_transactions(
        self,
        subject_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Sequence[Transaction]:
        return await self._repository.get_by_subject_id(
            subject_id, start_date, end_date
        )
