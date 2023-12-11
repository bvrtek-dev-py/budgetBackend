from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from budgetBackend.modules.transaction.models import Transaction


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
        result = await self._session.execute(select(Transaction))

        return result.scalars().all()

    async def get_by_id(self, transaction_id: int) -> Transaction | None:
        return await self._session.get(Transaction, transaction_id)
