from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, condecimal


class TransactionTransferRequest(BaseModel):
    name: str = Field(min_length=2)
    value: Decimal = condecimal(max_digits=10, decimal_places=2)  # type: ignore
    description: str = Field(min_length=2, max_length=2000)
    date: date
