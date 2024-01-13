# pylint: disable=E1102
from datetime import date, datetime
from decimal import Decimal
from typing import Sequence, Optional

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.modules.transaction.enums import TransactionType
from backend.modules.transaction.filters import filter_query_by_date_range
from backend.modules.transaction.interfaces import TransactionRepositoryInterface
from backend.modules.transaction.models import Transaction


class TransactionRepository(TransactionRepositoryInterface):
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

    async def get_by_user_id(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Sequence[Transaction]:
        query = select(Transaction).where(Transaction.user_id == user_id)

        query = filter_query_by_date_range(query, start_date, end_date)

        result = await self._session.execute(
            query.options(
                selectinload(Transaction.user),
                selectinload(Transaction.wallet),
                selectinload(Transaction.subject),
            )
        )

        return result.scalars().all()

    async def get_by_wallet_id(
        self, wallet_id: int, start_date: Optional[date], end_date: Optional[date]
    ) -> Sequence[Transaction]:
        query = select(Transaction).where(Transaction.wallet_id == wallet_id)

        query = filter_query_by_date_range(query, start_date, end_date)

        result = await self._session.execute(
            query.options(
                selectinload(Transaction.user),
                selectinload(Transaction.wallet),
                selectinload(Transaction.subject),
            )
        )

        return result.scalars().all()

    async def get_by_subject_id(
        self, subject_id: int, start_date: Optional[date], end_date: Optional[date]
    ) -> Sequence[Transaction]:
        query = select(Transaction).where(Transaction.subject_id == subject_id)

        query = filter_query_by_date_range(query, start_date, end_date)

        result = await self._session.execute(
            query.options(
                selectinload(Transaction.user),
                selectinload(Transaction.wallet),
                selectinload(Transaction.subject),
            )
        )

        return result.scalars().all()

    async def get_sum_value_by_type_and_user_id(
        self,
        user_id: int,
        transaction_type: TransactionType,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Decimal:
        query = select(func.sum(Transaction.value)).filter(
            (Transaction.type == transaction_type) & (Transaction.user_id == user_id)
        )

        query = filter_query_by_date_range(query, start_date, end_date)

        result = await self._session.execute(query)

        return result.scalar() or Decimal(0)

    async def get_sum_value_by_wallet_id_and_type(
        self,
        wallet_id: int,
        transaction_type: TransactionType,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Decimal:
        query = select(func.sum(Transaction.value)).where(
            (Transaction.wallet_id == wallet_id)
            & (Transaction.type == transaction_type)
        )

        query = filter_query_by_date_range(query, start_date, end_date)

        result = await self._session.execute(query)

        return result.scalar() or Decimal("0.0")
