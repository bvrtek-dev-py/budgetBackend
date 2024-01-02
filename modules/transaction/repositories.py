from datetime import date
from typing import Sequence, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.modules.subject.models import Subject
from backend.modules.transaction.models import Transaction
from backend.modules.user.models import User
from backend.modules.wallet.models import Wallet


class TransactionRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, transaction: Transaction) -> Transaction:
        self._session.add(transaction)
        await self._session.commit()

        return transaction

    async def update(self, transaction: Transaction) -> Transaction:
        await self._session.commit()
        await self._session.refresh(transaction)

        return transaction

    async def delete(self, transaction: Transaction) -> None:
        await self._session.delete(transaction)
        await self._session.commit()

    async def get_all(self) -> Sequence[Transaction]:
        result = await self._session.execute(
            select(Transaction).options(
                selectinload(Transaction.user),
                selectinload(Transaction.wallet),
                selectinload(Transaction.subject),
            )
        )

        return result.scalars().all()

    async def get_by_id(self, transaction_id: int) -> Transaction | None:
        result = await self._session.execute(
            select(Transaction)
            .where((Transaction.id == transaction_id))
            .options(
                selectinload(Transaction.user),
                selectinload(Transaction.wallet),
                selectinload(Transaction.subject),
            )
        )

        return result.scalars().first()

    async def get_by_name_and_wallet_and_type(
        self, name: str, wallet_id: int, transaction_date: date
    ) -> Transaction | None:
        result = await self._session.execute(
            select(Transaction)
            .where(
                (Transaction.name == name)
                & (Transaction.wallet_id == wallet_id)
                & (Transaction.date == transaction_date)
            )
            .options(
                selectinload(Transaction.user),
                selectinload(Transaction.wallet),
                selectinload(Transaction.subject),
            )
        )

        return result.scalars().first()

    async def get_user_transactions(
        self,
        user: User,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Sequence[Transaction]:
        query = select(Transaction).where(Transaction.user_id == user.id)

        if start_date is not None:
            query = query.where(Transaction.date >= start_date)

        if end_date is not None:
            query = query.where(Transaction.date <= end_date)

        result = await self._session.execute(
            query.options(
                selectinload(Transaction.user),
                selectinload(Transaction.wallet),
                selectinload(Transaction.subject),
            )
        )

        return result.scalars().all()

    async def get_wallet_transactions(
        self, wallet: Wallet, start_date: Optional[date], end_date: Optional[date]
    ) -> Sequence[Transaction]:
        query = select(Transaction).where(Transaction.wallet_id == wallet.id)

        if start_date is not None:
            query = query.where(Transaction.date >= start_date)

        if end_date is not None:
            query = query.where(Transaction.date <= end_date)

        result = await self._session.execute(
            query.options(
                selectinload(Transaction.user),
                selectinload(Transaction.wallet),
                selectinload(Transaction.subject),
            )
        )

        return result.scalars().all()

    async def get_subject_transactions(
        self, subject: Subject, start_date: Optional[date], end_date: Optional[date]
    ) -> Sequence[Transaction]:
        query = select(Transaction).where(Transaction.subject_id == subject.id)

        if start_date is not None:
            query = query.where(Transaction.date >= start_date)

        if end_date is not None:
            query = query.where(Transaction.date <= end_date)

        result = await self._session.execute(
            query.options(
                selectinload(Transaction.user),
                selectinload(Transaction.wallet),
                selectinload(Transaction.subject),
            )
        )

        return result.scalars().all()
