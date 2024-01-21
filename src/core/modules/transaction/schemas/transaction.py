from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel

from backend.src.core.modules.transaction.enums import TransactionType


class TransactionBaseDTO(BaseModel):
    name: str
    value: Decimal
    description: str
    date: date

    class ConfigDict:
        frozen = True


class TransactionCreateDTO(TransactionBaseDTO):
    type: TransactionType
    subject_id: int
    category_id: int


class TransactionUpdateDTO(TransactionBaseDTO):
    subject_id: int
    category_id: int


class TransactionTransferDTO(TransactionBaseDTO):
    pass


class TransactionValueSumDTO(BaseModel):
    incomes: Decimal
    expenses: Decimal
    transfer_incomes: Optional[Decimal] = None
    transfer_expenses: Optional[Decimal] = None
