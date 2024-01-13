from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from backend.modules.transaction.enums import TransactionType


class TransactionBaseRequest(BaseModel):
    name: str
    value: Decimal
    description: str
    date: date
    subject_id: int
    category_id: int


class TransactionCreateRequest(TransactionBaseRequest):
    type: TransactionType


class TransactionUpdateRequest(TransactionBaseRequest):
    pass
