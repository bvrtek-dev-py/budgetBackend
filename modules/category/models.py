from sqlalchemy import String, Enum
from sqlalchemy.orm import MappedColumn, mapped_column

from backend.database.base import BaseModel
from backend.modules.transaction.enums import TransactionType


class Category(BaseModel):
    __tablename__ = "categories"

    name: MappedColumn[str] = mapped_column(String(50))
    transaction_type: MappedColumn[TransactionType] = mapped_column(
        Enum(
            TransactionType,
            create_constraint=True,
            validate_strings=True,
        )
    )
