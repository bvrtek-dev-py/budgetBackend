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

    class ConfigDict:
        frozen = True


class TransactionCreateRequest(TransactionBaseRequest):
    type: TransactionType

    class ConfigDict:
        frozen = True


class TransactionUpdateRequest(TransactionBaseRequest):
    pass

    class ConfigDict:
        frozen = True
