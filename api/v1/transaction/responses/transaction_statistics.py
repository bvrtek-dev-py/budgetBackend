from decimal import Decimal
from typing import Dict

from pydantic import BaseModel


class TransactionStatisticResponse(BaseModel):
    balance: Decimal
    incomes: Decimal
    expenses: Decimal

    class ConfigDict:
        frozen = True
        orm_mode = True


class WalletTransactionStatisticResponse(TransactionStatisticResponse):
    transfers: Decimal

    class ConfigDict:
        frozen = True
        orm_mode = True


class WalletTransactionStatisticsResponse(BaseModel):
    total: WalletTransactionStatisticResponse
    monthly: Dict[str, WalletTransactionStatisticResponse]

    class ConfigDict:
        frozen = True
        orm_mode = True


class UserTransactionStatisticsResponse(BaseModel):
    total: TransactionStatisticResponse
    monthly: Dict[str, TransactionStatisticResponse]

    class ConfigDict:
        frozen = True
        orm_mode = True
