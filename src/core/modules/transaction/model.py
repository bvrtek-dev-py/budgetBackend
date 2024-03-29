from datetime import date
from decimal import Decimal

from sqlalchemy import (
    String,
    DECIMAL,
    Text,
    Enum,
    Date,
    ForeignKey,
    Integer,
    UniqueConstraint,
    Boolean,
)
from sqlalchemy.orm import MappedColumn, mapped_column, relationship

from backend.src.database.base import BaseModel
from backend.src.core.modules.transaction.enum import TransactionType


class Transaction(BaseModel):
    __tablename__ = "transactions"
    __table_args__ = (
        UniqueConstraint(
            "name",
            "wallet_id",
            "date",
            name="unique_name_wallet_date",
        ),
    )

    name: MappedColumn[str] = mapped_column(String(50))
    value: MappedColumn[Decimal] = mapped_column(DECIMAL(10, 2))
    description: MappedColumn[str] = mapped_column(Text(2000), default="")
    date: MappedColumn[date] = mapped_column(Date)
    type: MappedColumn[TransactionType] = mapped_column(
        Enum(
            TransactionType,
            create_constraint=True,
            validate_strings=True,
        )
    )
    is_transfer: MappedColumn[bool] = mapped_column(Boolean, default=False)

    user_id: MappedColumn[int] = mapped_column(Integer, ForeignKey("users.id"))
    wallet_id: MappedColumn[int] = mapped_column(Integer, ForeignKey("wallets.id"))
    subject_id: MappedColumn[int] = mapped_column(
        Integer, ForeignKey("subjects.id"), nullable=True
    )
    category_id: MappedColumn[int] = mapped_column(
        Integer, ForeignKey("categories.id"), nullable=True
    )

    user: MappedColumn["User"] = relationship(back_populates="transactions")  # type: ignore
    wallet: MappedColumn["Wallet"] = relationship(back_populates="transactions")  # type: ignore
    subject: MappedColumn["Subject"] = relationship(back_populates="transactions")  # type: ignore
    category: MappedColumn["Category"] = relationship(back_populates="transactions")  # type: ignore
