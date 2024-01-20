from datetime import date
from typing import Optional, Sequence

from backend.src.core.modules.subject.models import Subject
from backend.src.core.modules.transaction.models import Transaction
from backend.src.core.modules.transaction.repositories import TransactionRepository
from backend.src.core.modules.user.models import User
from backend.src.core.modules.wallet.models import Wallet


class TransactionQueryService:
    def __init__(self, repository: TransactionRepository):
        self._repository = repository

    async def get_user_transactions(
        self,
        user: User,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Sequence[Transaction]:
        return await self._repository.get_by_user_id(user.id, start_date, end_date)

    async def get_wallet_transactions(
        self,
        wallet: Wallet,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Sequence[Transaction]:
        return await self._repository.get_by_wallet_id(wallet.id, start_date, end_date)

    async def get_subject_transactions(
        self,
        subject: Subject,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Sequence[Transaction]:
        return await self._repository.get_by_subject_id(
            subject.id, start_date, end_date
        )
