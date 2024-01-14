# pylint: disable=E1102
import asyncio
from datetime import date, datetime
from decimal import Decimal
from typing import Sequence, Optional, Dict

from sqlalchemy import select, func, Select
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

    async def get_sum_values_by_user_id(
        self,
        user_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Decimal]:
        async with self._session.begin():
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

            return {
                "incomes": incomes,
                "expenses": expenses,
            }

    async def get_sum_values_by_wallet_id(
        self,
        wallet_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> Dict[str, Decimal]:
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

        return {
            "incomes": incomes,
            "expenses": expenses,
            "transfer_incomes": transfer_income,
            "transfer_expenses": transfer_expense,
        }

    async def _execute_sum_query(self, query) -> Decimal:
        result = await self._session.execute(query)
        return result.scalar() or Decimal("0.0")

    def _build_sum_query_with_wallet_id(
        self,
        wallet_id: int,
        transaction_type: TransactionType,
        is_transfer: bool,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> select:
        query = self._build_sum_base_query(transaction_type, is_transfer)
        query = self._apply_wallet_id_filter(query, wallet_id)
        query = filter_query_by_date_range(query, start_date, end_date)

        return query

    def _build_sum_query_with_user_id(
        self,
        user_id: int,
        transaction_type: TransactionType,
        is_transfer: bool,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> select:
        query = self._build_sum_base_query(transaction_type, is_transfer)
        query = self._apply_user_id_filter(query, user_id)
        query = filter_query_by_date_range(query, start_date, end_date)

        return query

    def _build_sum_base_query(
        self, transaction_type: TransactionType, is_transfer: bool
    ) -> Select:
        return select(func.sum(Transaction.value)).filter(
            (Transaction.type == transaction_type)
            & (Transaction.is_transfer == is_transfer)
        )

    def _apply_wallet_id_filter(self, query: select, wallet_id: int) -> Select:
        return query.filter(Transaction.wallet_id == wallet_id)

    def _apply_user_id_filter(self, query: Select, user_id: int) -> Select:
        return query.filter(Transaction.user_id == user_id)
