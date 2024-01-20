from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from backend.src.core.modules.transaction.enums import TransactionType


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


class TransactionTransferDTO(BaseModel):
    name: str
    value: Decimal
    description: str
    date: date


class TransactionValueSumDTO(BaseModel):
    incomes: Decimal
    expenses: Decimal
    transfer_incomes: Optional[Decimal] = None
    transfer_expenses: Optional[Decimal] = None
