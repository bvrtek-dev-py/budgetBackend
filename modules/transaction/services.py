from datetime import date
from decimal import Decimal
from typing import Sequence, Optional

from backend.modules.common.exceptions import ObjectDoesNotExist, ObjectAlreadyExists
from backend.modules.subject.models import Subject
from backend.modules.transaction.enums import TransactionType
from backend.modules.transaction.models import Transaction
from backend.modules.transaction.repositories import TransactionRepository
from backend.modules.user.models import User
from backend.modules.wallet.models import Wallet


class TransactionService:
    def __init__(self, repository: TransactionRepository):
        self._repository = repository

    async def create(  # pylint: disable=too-many-arguments
        self,
        name: str,
        value: Decimal,
        transaction_type: TransactionType,
        description: str,
        transaction_date: date,
        user_id: int,
        wallet_id: int,
        subject_id: int
    ) -> Transaction:
        if await self._check_constraint_blockade(name, transaction_date, wallet_id):
            raise ObjectAlreadyExists

        transaction = Transaction(
            name=name,
            value=value,
            type=transaction_type,
            description=description,
            date=transaction_date,
            user_id=user_id,
            wallet_id=wallet_id,
            subject_id=subject_id
        )

        return await self._repository.save(transaction)

    async def update(  # pylint: disable=too-many-arguments
        self,
        transaction_id: int,
        name: str,
        value: Decimal,
        description: str,
        transaction_date: date,
        subject_id: int
    ) -> Transaction:
        transaction = await self.get_by_id(transaction_id)

        if await self._check_constraint_blockade(
            name, transaction_date, transaction.wallet_id, transaction_id
        ):
            raise ObjectAlreadyExists

        transaction.name = name
        transaction.value = value
        transaction.description = description
        transaction.date = transaction_date
        transaction.subject_id = subject_id

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
        self, subject: Subject, start_date: date, end_date: date
    ) -> Sequence[Transaction]:
        return await self._repository.get_subject_transactions(
            subject, start_date, end_date
        )
