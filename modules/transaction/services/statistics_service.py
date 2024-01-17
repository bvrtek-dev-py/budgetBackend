from datetime import datetime
from decimal import Decimal
from typing import Dict

from dateutil.relativedelta import relativedelta

from backend.modules.common.utils import get_last_day_of_month
from backend.modules.transaction.repositories import TransactionRepository
from backend.modules.transaction.schemas.statistics import (
    TransactionStatisticsDTO,
    TransactionStatisticDTO,
)
from backend.modules.transaction.schemas.transaction import TransactionValueSumDTO


class TransactionStatisticsService:
    def __init__(self, repository: TransactionRepository):
        self._repository = repository

    async def get_wallet_balance(self, wallet_id: int) -> TransactionStatisticDTO:
        result = await self._repository.get_sum_values_by_wallet_id(wallet_id)

        return self._update_transaction_statistic_dto(
            statistic_dto=TransactionStatisticDTO(transfers=Decimal("0.0")),
            update_data=result,
        )

    async def get_user_balance(self, user_id: int) -> TransactionStatisticDTO:
        result = await self._repository.get_sum_values_by_user_id(user_id)

        return self._update_transaction_statistic_dto(
            statistic_dto=TransactionStatisticDTO(), update_data=result
        )

    async def get_statistics_for_user(
        self, user_id: int, start_date: datetime
    ) -> TransactionStatisticsDTO:
        statistics = TransactionStatisticsDTO(
            total=TransactionStatisticDTO(),
            monthly={},
        )

        while start_date <= datetime.now():
            end_date = get_last_day_of_month(start_date)
            result = await self._repository.get_sum_values_by_user_id(
                user_id, start_date, end_date
            )

            statistics.monthly[
                start_date.strftime("%Y-%m")
            ] = self._update_transaction_statistic_dto(
                statistic_dto=TransactionStatisticDTO(), update_data=result
            )
            self._update_transaction_statistic_dto(
                statistic_dto=statistics.total, update_data=result
            )

            start_date += relativedelta(months=1)

        return statistics

    async def get_statistics_for_wallet(
        self, wallet_id: int, start_date: datetime
    ) -> TransactionStatisticsDTO:
        statistics = TransactionStatisticsDTO(
            total=TransactionStatisticDTO(transfers=Decimal("0.0")),
            monthly={},
        )

        while start_date <= datetime.now():
            end_date = get_last_day_of_month(start_date)
            result = await self._repository.get_sum_values_by_wallet_id(
                wallet_id, start_date, end_date
            )

            statistics.monthly[
                start_date.strftime("%Y-%m")
            ] = self._update_transaction_statistic_dto(
                statistic_dto=TransactionStatisticDTO(transfers=Decimal("0.0")),
                update_data=result,
            )
            self._update_transaction_statistic_dto(statistics.total, result)

            start_date += relativedelta(months=1)

        return statistics

    def _update_monthly_statistics(
        self,
        monthly: Dict[str, TransactionStatisticDTO],
        start_date: datetime,
        update_data: TransactionValueSumDTO,
        with_transfer: bool,
    ) -> None:
        month_stats_dto = TransactionStatisticDTO()

        if with_transfer:
            month_stats_dto.transfers = Decimal("0.0")

        month_key = start_date.strftime("%Y-%m")
        monthly[month_key] = self._update_transaction_statistic_dto(
            month_stats_dto, update_data
        )

    def _update_transaction_statistic_dto(
        self,
        statistic_dto: TransactionStatisticDTO,
        update_data: TransactionValueSumDTO,
    ) -> TransactionStatisticDTO:
        statistic_dto.balance += update_data.incomes - update_data.expenses
        statistic_dto.incomes += update_data.incomes
        statistic_dto.expenses += update_data.expenses

        if statistic_dto.transfers is not None:
            statistic_dto.balance += (
                update_data.transfer_incomes - update_data.transfer_expenses  # type: ignore
            )
            statistic_dto.transfers += (
                update_data.transfer_incomes - update_data.transfer_expenses  # type: ignore
            )

        return statistic_dto
