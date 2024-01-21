from datetime import date
from decimal import Decimal

from pydantic import BaseModel


class TransactionTransferResponse(BaseModel):
    name: str
    value: Decimal
    description: str
    date: date

    class ConfigDict:
        frozen = True
