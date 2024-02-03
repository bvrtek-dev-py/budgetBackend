from datetime import date
from typing import Optional

from backend.src.core.modules.common.exceptions import (
    ObjectAlreadyExists,
)
from backend.src.core.modules.transaction.model import Transaction
from backend.src.core.modules.transaction.repository import TransactionRepository
from backend.src.core.modules.transaction.schemas.transaction import (
    TransactionCreateDTO,
    TransactionUpdateDTO,
)
from backend.src.core.modules.transaction.use_case import TransactionRetrievalUseCase


class TransactionService:
    def __init__(
        self,
        repository: TransactionRepository,
        retrieval_use_case: TransactionRetrievalUseCase,
    ):
        self._repository = repository
        self._retrieval_use_case = retrieval_use_case

    async def create(
        self, wallet_id: int, user_id: int, request_dto: TransactionCreateDTO
    ) -> Transaction:
        if await self._check_constraint_blockade(
            request_dto.name, request_dto.date, wallet_id
        ):
            raise ObjectAlreadyExists()

        transaction = Transaction(
            **request_dto.model_dump(), wallet_id=wallet_id, user_id=user_id
        )

        return await self._repository.save(transaction)

    async def update(
        self, transaction_id: int, request_dto: TransactionUpdateDTO
    ) -> Transaction:
        transaction = await self.get_by_id(transaction_id)

        if await self._check_constraint_blockade(
            request_dto.name, request_dto.date, transaction.wallet_id, transaction_id
        ):
            raise ObjectAlreadyExists()

        for key, value in request_dto.model_dump().items():
            setattr(transaction, key, value)

        return await self._repository.update(transaction)

    async def delete(self, transaction_id: int) -> None:
        transaction = await self.get_by_id(transaction_id)

        return await self._repository.delete(transaction)

    async def get_by_id(self, transaction_id: int) -> Transaction:
        return await self._retrieval_use_case.get_by_id(transaction_id)

    async def _check_constraint_blockade(
        self,
        name: str,
        transaction_date: date,
        wallet_id: int,
        excluded_id: Optional[int] = None,
    ) -> bool:
        transaction = await self._repository.get_by_name_and_wallet_and_type(
            name, wallet_id, transaction_date
        )

        if transaction is None:
            return False

        if transaction.id == excluded_id:
            return False

        return True
