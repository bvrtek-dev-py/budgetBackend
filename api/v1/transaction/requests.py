from decimal import Decimal

from pydantic import BaseModel

from backend.modules.transaction.enums import TransactionType


class TransactionCreateRequest(BaseModel):
    name: str
    value: Decimal
    type: TransactionType
    description: str


class TransactionUpdateRequest(BaseModel):
    name: str
    value: Decimal
    description: str
