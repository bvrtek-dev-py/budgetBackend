# pylint: disable=R0913
import asyncio
from datetime import date, datetime
from decimal import Decimal
from typing import Sequence, Optional

from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.modules.transaction.builders.fetch_query import (
    TransactionFetchQueryBuilder,
)
from backend.modules.transaction.builders.sum_query import (
    TransactionValueSumQueryBuilder,
)
from backend.modules.transaction.enums import TransactionType
from backend.modules.transaction.interfaces import TransactionRepositoryInterface
from backend.modules.transaction.models import Transaction
from backend.modules.transaction.schemas.transaction import TransactionValueSumDTO


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
            self._load_related_models(select(Transaction))
        )

        return result.scalars().all()

    async def get_by_id(self, transaction_id: int) -> Transaction | None:
        result = await self._session.execute(
            self._load_related_models(
                select(Transaction).filter((Transaction.id == transaction_id))
            )
        )

        return result.scalars().first()

    async def get_by_name_and_wallet_and_type(
        self, name: str, wallet_id: int, transaction_date: date
    ) -> Transaction | None:
        query = (
            TransactionFetchQueryBuilder()
            .apply_name(name)
            .apply_wallet_id_filter(wallet_id)
            .apply_date(transaction_date)
            .build()
        )

        result = await self._session.execute(self._load_related_models(query))

        return result.scalars().first()

    async def get_by_user_id(
        self,
        user_id: int,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Sequence[Transaction]:
        query = (
            TransactionFetchQueryBuilder()
            .apply_user_id_filter(user_id)
            .apply_start_date_filter(start_date)
            .apply_end_date_filter(end_date)
            .build()
        )

        result = await self._session.execute(self._load_related_models(query))

        return result.scalars().all()

    async def get_by_wallet_id(
        self, wallet_id: int, start_date: Optional[date], end_date: Optional[date]
    ) -> Sequence[Transaction]:
        query = (
            TransactionFetchQueryBuilder()
            .apply_wallet_id_filter(wallet_id)
            .apply_start_date_filter(start_date)
            .apply_end_date_filter(end_date)
            .build()
        )

        result = await self._session.execute(self._load_related_models(query))

        return result.scalars().all()

    async def get_by_subject_id(
        self, subject_id: int, start_date: Optional[date], end_date: Optional[date]
    ) -> Sequence[Transaction]:
        query = (
            TransactionFetchQueryBuilder()
            .apply_subject_id_filter(subject_id)
            .apply_start_date_filter(start_date)
            .apply_end_date_filter(end_date)
            .build()
        )

        result = await self._session.execute(self._load_related_models(query))

        return result.scalars().all()

    async def get_sum_values_by_user_id(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> TransactionValueSumDTO:
        income_query = self._build_sum_query_with_user_id(
            user_id, TransactionType.INCOME, False, start_date, end_date
        )
        expense_query = self._build_sum_query_with_user_id(
            user_id, TransactionType.EXPENSE, False, start_date, end_date
        )

        incomes, expenses = await asyncio.gather(
            self._execute_sum_query(income_query),
            self._execute_sum_query(expense_query),
        )

        return TransactionValueSumDTO(incomes=incomes, expenses=expenses)

    async def get_sum_values_by_wallet_id(
        self,
        wallet_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> TransactionValueSumDTO:
        income_query = self._build_sum_query_with_wallet_id(
            wallet_id, TransactionType.INCOME, False, start_date, end_date
        )
        expense_query = self._build_sum_query_with_wallet_id(
            wallet_id, TransactionType.EXPENSE, False, start_date, end_date
        )
        transfer_income_query = self._build_sum_query_with_wallet_id(
            wallet_id, TransactionType.INCOME, True, start_date, end_date
        )
        transfer_expense_query = self._build_sum_query_with_wallet_id(
            wallet_id, TransactionType.EXPENSE, True, start_date, end_date
        )

        incomes, expenses, transfer_income, transfer_expense = await asyncio.gather(
            self._execute_sum_query(income_query),
            self._execute_sum_query(expense_query),
            self._execute_sum_query(transfer_income_query),
            self._execute_sum_query(transfer_expense_query),
        )

        return TransactionValueSumDTO(
            incomes=incomes,
            expenses=expenses,
            transfer_incomes=transfer_income,
            transfer_expenses=transfer_expense,
        )

    def _build_sum_query_with_wallet_id(
        self,
        wallet_id: int,
        transaction_type: TransactionType,
        is_transfer: bool,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Select:
        return (
            TransactionValueSumQueryBuilder()
            .apply_transaction_type_filter(transaction_type)
            .apply_is_transfer_filter(is_transfer)
            .apply_wallet_id_filter(wallet_id)
            .apply_start_date_filter(start_date)
            .apply_end_date_filter(end_date)
            .build()
        )

    def _build_sum_query_with_user_id(
        self,
        user_id: int,
        transaction_type: TransactionType,
        is_transfer: bool,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Select:
        return (
            TransactionValueSumQueryBuilder()
            .apply_transaction_type_filter(transaction_type)
            .apply_is_transfer_filter(is_transfer)
            .apply_user_id_filter(user_id)
            .apply_start_date_filter(start_date)
            .apply_end_date_filter(end_date)
            .build()
        )

    async def _execute_sum_query(self, query: Select) -> Decimal:
        result = await self._session.execute(query)
        return result.scalar() or Decimal("0.0")

    def _load_related_models(self, query: Select) -> Select:
        return query.options(
            selectinload(Transaction.user),
            selectinload(Transaction.wallet),
            selectinload(Transaction.subject),
            selectinload(Transaction.category),
        )
