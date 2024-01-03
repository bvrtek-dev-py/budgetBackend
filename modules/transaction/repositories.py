from datetime import date
from decimal import Decimal
from typing import Sequence, Optional, Any

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.modules.subject.models import Subject
from backend.modules.transaction.enums import TransactionType
from backend.modules.transaction.filters import filter_query_by_date_range
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

        query = filter_query_by_date_range(query, start_date, end_date)

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

        query = filter_query_by_date_range(query, start_date, end_date)

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

        query = filter_query_by_date_range(query, start_date, end_date)

        result = await self._session.execute(
            query.options(
                selectinload(Transaction.user),
                selectinload(Transaction.wallet),
                selectinload(Transaction.subject),
            )
        )

        return result.scalars().all()

    # pylint: disable=E1102
    async def get_sum_value_by_type_and_wallet_id(
        self, wallet_id: int, transaction_type: TransactionType
    ) -> Decimal:
        result: Any = await self._session.execute(
            select(func.sum(Transaction.value)).filter(
                (Transaction.type == transaction_type)
                & (Transaction.wallet_id == wallet_id)
            )
        )

        return result.scalar() or Decimal(0)

    async def get_sum_value_by_type_and_user_id(
        self, user_id, transaction_type: TransactionType
    ) -> Decimal:
        result: Any = await self._session.execute(
            select(func.sum(Transaction.value)).filter(
                (Transaction.type == transaction_type)
                & (Transaction.user_id == user_id)
            )
        )

        return result.scalar() or Decimal(0)
