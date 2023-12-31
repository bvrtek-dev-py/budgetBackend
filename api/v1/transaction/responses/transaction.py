from datetime import datetime, date as date_type
from decimal import Decimal

from pydantic import BaseModel

from backend.modules.transaction.enums import TransactionType


class TransactionBaseResponse(BaseModel):
    id: int
    name: str
    value: Decimal
    type: TransactionType
    date: date_type
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        frozen = True
        orm_mode = True
