from decimal import Decimal

from sqlalchemy import String, DECIMAL, Text, Enum
from sqlalchemy.orm import MappedColumn, mapped_column

from budgetBackend.database.base import BaseModel
from budgetBackend.modules.transaction.enums import TransactionType


class Transaction(BaseModel):
    __tablename__ = "transactions"

    name: MappedColumn[str] = mapped_column(String(50))
    value: MappedColumn[Decimal] = mapped_column(DECIMAL(10, 2))
    description: MappedColumn[str] = mapped_column(Text(2000), default="")
    type: MappedColumn[TransactionType] = mapped_column(
        Enum(
            TransactionType,
            create_constraint=True,
            validate_strings=True,
        )
    )
