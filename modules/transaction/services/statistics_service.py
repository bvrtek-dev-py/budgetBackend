from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional

from dateutil.relativedelta import relativedelta

from backend.modules.common.utils import get_last_day_of_month
from backend.modules.transaction.repositories import TransactionRepository
from backend.modules.transaction.types import StatisticsType, MonthlyType, TotalType


class TransactionStatisticsService:
    def __init__(self, repository: TransactionRepository):
        self._repository = repository

    async def get_wallet_balance(self, wallet_id: int) -> Dict[str, Decimal]:
        results = await self._repository.get_sum_values_by_wallet_id(wallet_id)
        transfer_balance = results["transfer_incomes"] - results["transfer_expenses"]

        return {
            "incomes": results["incomes"],
            "expenses": results["expenses"],
            "balance": results["incomes"] - results["expenses"] + transfer_balance,
            "transfers": transfer_balance,
        }

    async def get_user_balance(self, user_id: int) -> Dict[str, Decimal]:
        results = await self._repository.get_sum_values_by_user_id(user_id)

        return {
            "incomes": results["incomes"],
            "expenses": results["expenses"],
            "balance": results["incomes"] - results["expenses"],
        }

    async def get_statistics_for_user(
        self, user_id: int, start_date: datetime
    ) -> StatisticsType:
        statistics = self._initialize_statistics(False)

        while start_date <= datetime.now():
            end_date = get_last_day_of_month(start_date)
            results = await self._repository.get_sum_values_by_user_id(
                user_id, start_date, end_date
            )

            self._update_statistics(
                statistics["monthly"],
                start_date,
                results["incomes"],
                results["expenses"],
            )
            self._update_total(
                statistics["total"], results["incomes"], results["expenses"]
            )

            start_date += relativedelta(months=1)

        return statistics

    async def get_statistics_for_wallet(
        self, wallet_id: int, start_date: datetime
    ) -> StatisticsType:
        statistics = self._initialize_statistics(True)

        while start_date <= datetime.now():
            end_date = get_last_day_of_month(start_date)
            results = await self._repository.get_sum_values_by_wallet_id(
                wallet_id, start_date, end_date
            )

            self._update_statistics(
                statistics["monthly"],
                start_date,
                results["incomes"],
                results["expenses"],
                transfer=results["transfer_incomes"] - results["transfer_expenses"],
            )
            self._update_total(
                statistics["total"],
                results["incomes"],
                results["expenses"],
                results["transfer_incomes"] - results["transfer_expenses"],
            )

            start_date += relativedelta(months=1)

        return statistics

    def _initialize_statistics(self, with_transfer: bool) -> StatisticsType:
        initial_values = {
            "total": {
                "balance": Decimal(0),
                "incomes": Decimal(0),
                "expenses": Decimal(0),
            },
            "monthly": {},
        }

        if with_transfer:
            initial_values["total"]["transfers"] = Decimal(0)

        return initial_values

    def _update_statistics(
        self,
        monthly: MonthlyType,
        start_date: datetime,
        incomes: Decimal,
        expenses: Decimal,
        transfer: Optional[Decimal] = None,
    ) -> None:
        month_key = start_date.strftime("%Y-%m")
        month_data = {
            "balance": incomes - expenses + (transfer or Decimal(0)),
            "incomes": incomes,
            "expenses": expenses,
        }

        if transfer is not None:
            month_data["transfers"] = transfer

        monthly[month_key] = month_data

    def _update_total(
        self,
        total: TotalType,
        incomes: Decimal,
        expenses: Decimal,
        transfer: Optional[Decimal] = None,
    ) -> None:
        total["incomes"] += incomes
        total["expenses"] += expenses
        total["balance"] += incomes - expenses + (transfer or Decimal(0))

        if transfer is not None:
            total["transfers"] += transfer
