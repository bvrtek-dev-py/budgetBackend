from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, condecimal

from backend.src.core.modules.transaction.enums import TransactionType


class TransactionBaseRequest(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    value: Decimal = condecimal(max_digits=12, decimal_places=2)  # type: ignore
    description: str = Field(min_length=2, max_length=2000)
    date: date
    subject_id: int = Field(gt=0)
    category_id: int = Field(gt=0)

    class ConfigDict:
        frozen = True


class TransactionCreateRequest(TransactionBaseRequest):
    type: TransactionType


class TransactionUpdateRequest(TransactionBaseRequest):
    pass
