from datetime import date
from typing import Optional, Sequence

from backend.modules.subject.models import Subject
from backend.modules.transaction.models import Transaction
from backend.modules.transaction.repositories import TransactionRepository
from backend.modules.user.models import User
from backend.modules.wallet.models import Wallet


class TransactionQueryService:
    def __init__(self, repository: TransactionRepository):
        self._repository = repository

    async def get_user_transactions(
        self,
        user: User,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Sequence[Transaction]:
        return await self._repository.get_user_transactions(user, start_date, end_date)

    async def get_wallet_transactions(
        self,
        wallet: Wallet,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Sequence[Transaction]:
        return await self._repository.get_wallet_transactions(
            wallet, start_date, end_date
        )

    async def get_subject_transactions(
        self,
        subject: Subject,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Sequence[Transaction]:
        return await self._repository.get_subject_transactions(
            subject, start_date, end_date
        )
