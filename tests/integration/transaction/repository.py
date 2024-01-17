from datetime import date, datetime
from decimal import Decimal
from typing import List, Sequence, Optional

from backend.modules.transaction.enums import TransactionType
from backend.modules.transaction.interfaces import TransactionRepositoryInterface
from backend.modules.transaction.models import Transaction
from backend.modules.transaction.schemas.transaction import TransactionValueSumDTO
from backend.tests.database import get_transaction_data


class InMemoryTransactionRepository(TransactionRepositoryInterface):
    def __init__(self):
        self.transactions: List[Transaction] = get_transaction_data()

    async def save(self, transaction: Transaction) -> Transaction:
        self.transactions.append(transaction)
        return transaction

    async def update(self, transaction: Transaction) -> Transaction:
        return transaction

    async def delete(self, transaction: Transaction) -> None:
        self.transactions.remove(transaction)

    async def get_all(self) -> Sequence[Transaction]:
        return self.transactions

    async def get_by_id(self, transaction_id: int) -> Transaction | None:
        for transaction in self.transactions:
            if transaction.id == transaction_id:
                return transaction

        return None

    async def get_by_name_and_wallet_and_type(
        self, name: str, wallet_id: int, transaction_date: date
    ) -> Transaction | None:
        for transaction in self.transactions:
            if (
                transaction.name == name
                and transaction.wallet_id == wallet_id
                and transaction.date == transaction_date
            ):
                return transaction

        return None

    async def get_by_user_id(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Sequence[Transaction]:
        filtered_transactions = []

        for transaction in self.transactions:
            is_matching_user = transaction.user_id == user_id
            is_within_date_range = (
                start_date is None or transaction.date >= start_date
            ) and (end_date is None or transaction.date <= end_date)

            if is_matching_user and is_within_date_range:
                filtered_transactions.append(transaction)

        return filtered_transactions

    async def get_by_wallet_id(
        self, wallet_id: int, start_date: Optional[date], end_date: Optional[date]
    ) -> Sequence[Transaction]:
        filtered_transactions = []

        for transaction in self.transactions:
            is_matching_wallet = transaction.wallet_id == wallet_id
            is_within_date_range = (
                start_date is None or transaction.date >= start_date
            ) and (end_date is None or transaction.date <= end_date)

            if is_matching_wallet and is_within_date_range:
                filtered_transactions.append(transaction)

        return filtered_transactions

    async def get_by_subject_id(
        self, subject_id: int, start_date: Optional[date], end_date: Optional[date]
    ) -> Sequence[Transaction]:
        filtered_transactions = []

        for transaction in self.transactions:
            is_matching_subject = transaction.subject_id == subject_id
            is_within_date_range = (
                start_date is None or transaction.date >= start_date
            ) and (end_date is None or transaction.date <= end_date)

            if is_matching_subject and is_within_date_range:
                filtered_transactions.append(transaction)

        return filtered_transactions

    async def get_sum_values_by_user_id(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> TransactionValueSumDTO:
        incomes = Decimal(
            sum(
                Decimal(transaction.value)
                for transaction in self.transactions
                if transaction.user_id == user_id
                and transaction.type == TransactionType.INCOME
                and (start_date is None or transaction.date >= start_date)
                and (end_date is None or transaction.date <= end_date)
            )
        )

        expenses = Decimal(
            sum(
                Decimal(transaction.value)
                for transaction in self.transactions
                if transaction.user_id == user_id
                and transaction.type == TransactionType.EXPENSE
                and (start_date is None or transaction.date >= start_date)
                and (end_date is None or transaction.date <= end_date)
            )
        )

        return TransactionValueSumDTO(incomes=incomes, expenses=expenses)

    async def get_sum_values_by_wallet_id(
        self,
        wallet_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> TransactionValueSumDTO:
        incomes = Decimal(
            sum(
                Decimal(transaction.value)
                for transaction in self.transactions
                if transaction.wallet_id == wallet_id
                and transaction.type == TransactionType.INCOME
                and (start_date is None or transaction.date >= start_date)
                and (end_date is None or transaction.date <= end_date)
            )
        )

        expenses = Decimal(
            sum(
                Decimal(transaction.value)
                for transaction in self.transactions
                if transaction.wallet_id == wallet_id
                and transaction.type == TransactionType.EXPENSE
                and (start_date is None or transaction.date >= start_date)
                and (end_date is None or transaction.date <= end_date)
            )
        )

        transfer_incomes = Decimal(
            sum(
                Decimal(transaction.value)
                for transaction in self.transactions
                if transaction.wallet_id == wallet_id
                and transaction.type == TransactionType.INCOME
                and transaction.is_transfer
                and (start_date is None or transaction.date >= start_date)
                and (end_date is None or transaction.date <= end_date)
            )
        )

        transfer_expenses = Decimal(
            sum(
                Decimal(transaction.value)
                for transaction in self.transactions
                if transaction.wallet_id == wallet_id
                and transaction.type == TransactionType.EXPENSE
                and transaction.is_transfer
                and (start_date is None or transaction.date >= start_date)
                and (end_date is None or transaction.date <= end_date)
            )
        )

        return TransactionValueSumDTO(
            incomes=incomes,
            expenses=expenses,
            transfer_expenses=transfer_expenses,
            transfer_incomes=transfer_incomes,
        )
