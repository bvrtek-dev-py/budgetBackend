from decimal import Decimal
from typing import Sequence

from budgetBackend.modules.common.exceptions import ObjectDoesNotExist
from budgetBackend.modules.transaction.enums import TransactionType
from budgetBackend.modules.transaction.models import Transaction
from budgetBackend.modules.transaction.repositories import TransactionRepository


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self._repository = repository

    async def create(
        self,
        name: str,
        value: Decimal,
        transaction_type: TransactionType,
        description: str,
    ) -> Transaction:
        transaction = Transaction(
            name=name, value=value, type=transaction_type, description=description
        )

        return await self._repository.save(transaction)

    async def update(
        self, transaction_id: int, name: str, value: Decimal, description: str
    ) -> Transaction:
        transaction = await self.get_by_id(transaction_id)

        transaction.name = name
        transaction.value = value
        transaction.description = description

        return await self._repository.update(transaction)

    async def delete(self, transaction_id: int) -> None:
        transaction = await self.get_by_id(transaction_id)

        return await self._repository.delete(transaction)

    async def get_by_id(self, transaction_id: int) -> Transaction:
        transaction = await self._repository.get_by_id(transaction_id)

        if transaction is None:
            raise ObjectDoesNotExist

        return transaction

    async def get_all(self) -> Sequence[Transaction]:
        return await self._repository.get_all()
