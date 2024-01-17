from decimal import Decimal
from typing import Optional, Dict

from pydantic import BaseModel


class TransactionStatisticDTO(BaseModel):
    balance: Decimal = Decimal(0)
    incomes: Decimal = Decimal(0)
    expenses: Decimal = Decimal(0)
    transfers: Optional[Decimal] = None


class TransactionStatisticsDTO(BaseModel):
    total: TransactionStatisticDTO
    monthly: Dict[str, TransactionStatisticDTO]
