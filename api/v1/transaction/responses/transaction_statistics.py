from decimal import Decimal
from typing import Dict

from pydantic import BaseModel


class TransactionStatisticResponse(BaseModel):
    balance: Decimal
    income: Decimal
    expense: Decimal

    class ConfigDict:
        frozen = True


class TransactionStatisticsResponse(BaseModel):
    total: TransactionStatisticResponse
    monthly: Dict[str, TransactionStatisticResponse]

    class ConfigDict:
        frozen = True
