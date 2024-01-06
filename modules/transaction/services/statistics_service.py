from datetime import datetime
from decimal import Decimal
from typing import Dict, Union

from dateutil.relativedelta import relativedelta

from backend.modules.common.utils import get_last_day_of_month
from backend.modules.transaction.enums import TransactionType
from backend.modules.transaction.repositories import TransactionRepository
from backend.modules.transaction.types import StatisticsType, MonthlyType, TotalType
from backend.modules.wallet.models import Wallet


class TransactionStatisticsService:
    def __init__(self, repository: TransactionRepository):
        self._repository = repository

    async def get_wallet_balance(self, wallet: Wallet) -> Dict[str, Decimal]:
        incomes = await self._repository.get_sum_value_by_wallet_id_and_type(
            wallet.id, TransactionType.INCOME
        )
        expenses = await self._repository.get_sum_value_by_wallet_id_and_type(
            wallet.id, TransactionType.EXPENSE
        )

        return {"income": incomes, "expense": expenses, "balance": incomes - expenses}

    async def get_user_balance(self, user_id: int) -> Dict[str, Decimal]:
        incomes = await self._repository.get_sum_value_by_type_and_user_id(
            user_id, TransactionType.INCOME
        )
        expenses = await self._repository.get_sum_value_by_type_and_user_id(
            user_id, TransactionType.EXPENSE
        )

        return {"income": incomes, "expense": expenses, "balance": incomes - expenses}

    async def get_statistics_for_user(
        self, user_id: int, start_date: datetime
    ) -> StatisticsType:
        statistics = self._initialize_statistics()

        while start_date <= datetime.now():
            end_date = get_last_day_of_month(start_date)

            income = await self._repository.get_sum_value_by_type_and_user_id(
                user_id, TransactionType.INCOME, start_date, end_date
            )
            expense = await self._repository.get_sum_value_by_type_and_user_id(
                user_id, TransactionType.EXPENSE, start_date, end_date
            )

            month_key = f"{start_date.year}-{start_date.month}"
            self._update_statistics(statistics["monthly"], month_key, income, expense)  # type: ignore
            self._update_total(statistics["total"], income, expense)  # type: ignore
            # Types are generally correct, ignored because mypy doesn't support selecting from union

            start_date += relativedelta(months=1)

        return statistics

    async def get_statistics_for_wallet(
        self, wallet_id: int, start_date: datetime
    ) -> StatisticsType:
        statistics = self._initialize_statistics()

        while start_date <= datetime.now():
            end_date = get_last_day_of_month(start_date)

            income = await self._repository.get_sum_value_by_wallet_id_and_type(
                wallet_id, TransactionType.INCOME, start_date, end_date
            )
            expense = await self._repository.get_sum_value_by_wallet_id_and_type(
                wallet_id, TransactionType.EXPENSE, start_date, end_date
            )

            month_key = f"{start_date.year}-{start_date.month}"
            self._update_statistics(statistics["monthly"], month_key, income, expense)  # type: ignore
            self._update_total(statistics["total"], income, expense)  # type: ignore
            # Types are generally correct, ignored because mypy doesn't support selecting from union

            start_date += relativedelta(months=1)

        return statistics

    def _initialize_statistics(
        self,
    ) -> StatisticsType:
        return {
            "total": {
                "balance": Decimal(0),
                "income": Decimal(0),
                "expense": Decimal(0),
            },
            "monthly": {},
        }

    def _update_statistics(
        self,
        monthly: MonthlyType,
        month_key: str,
        income: Decimal,
        expense: Decimal,
    ) -> None:
        monthly[month_key] = {
            "balance": income - expense,
            "income": income,
            "expense": expense,
        }

    def _update_total(
        self, total: TotalType, income: Decimal, expense: Decimal
    ) -> None:
        total["balance"] += income - expense
        total["expense"] += expense
        total["income"] += income
