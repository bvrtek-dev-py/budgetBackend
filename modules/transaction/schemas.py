from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from backend.modules.transaction.enums import TransactionType


class TransactionCreateDTO(BaseModel):
    name: str
    value: Decimal
    type: TransactionType
    description: str
    date: date
    subject_id: int
    category_id: int


class TransactionUpdateDTO(BaseModel):
    name: str
    value: Decimal
    description: str
    date: date
    subject_id: int
    category_id: int
