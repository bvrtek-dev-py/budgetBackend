from typing import List

from sqlalchemy import String, Enum, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import MappedColumn, mapped_column, relationship

from backend.database.base import BaseModel
from backend.modules.transaction.enums import TransactionType


class Category(BaseModel):
    __tablename__ = "categories"
    __table_args__ = (UniqueConstraint("name", "user_id", name="unique_user_name"),)

    name: MappedColumn[str] = mapped_column(String(50))
    transaction_type: MappedColumn[TransactionType] = mapped_column(
        Enum(
            TransactionType,
            create_constraint=True,
            validate_strings=True,
        )
    )
    user_id: MappedColumn[int] = mapped_column(Integer, ForeignKey("users.id"))

    user: MappedColumn["User"] = relationship(back_populates="categories")  # type: ignore
    transactions: MappedColumn[List["Transaction"]] = relationship(  # type: ignore
        back_populates="category"
    )
