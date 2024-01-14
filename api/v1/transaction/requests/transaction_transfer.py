from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class TransactionTransferRequest(BaseModel):
    name: str
    value: Decimal
    description: str
    date: date
