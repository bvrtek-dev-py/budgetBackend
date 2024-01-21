from datetime import datetime, date as date_type
from decimal import Decimal

from pydantic import BaseModel

from backend.src.core.modules.transaction.enum import TransactionType


class TransactionBaseResponse(BaseModel):
    id: int
    name: str
    value: Decimal
    type: TransactionType
    description: str
    date: date_type
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        frozen = True
