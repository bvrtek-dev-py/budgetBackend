from datetime import date
from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.modules.transaction.models import Transaction


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
                selectinload(Transaction.user), selectinload(Transaction.user)
            )
        )

        return result.scalars().all()

    async def get_by_id(self, transaction_id: int) -> Transaction | None:
        result = await self._session.execute(
            select(Transaction)
            .where((Transaction.id == transaction_id))
            .options(selectinload(Transaction.user), selectinload(Transaction.user))
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
            .options(selectinload(Transaction.user), selectinload(Transaction.user))
        )

        return result.scalars().first()
