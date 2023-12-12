from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from backend.modules.transaction.enums import TransactionType


class TransactionBaseResponse(BaseModel):
    id: int
    name: str
    value: Decimal
    type: TransactionType
    created_at: datetime
    updated_at: datetime
