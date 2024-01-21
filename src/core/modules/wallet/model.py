from typing import List

from sqlalchemy import String, Text, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import MappedColumn, mapped_column, relationship

from backend.src.database.base import BaseModel


class Wallet(BaseModel):
    __tablename__ = "wallets"
    __table_args__ = (UniqueConstraint("name", "user_id", name="unique_user_name"),)

    name: MappedColumn[str] = mapped_column(String(50))
    description: MappedColumn[str] = mapped_column(Text(2000), default="")
    user_id: MappedColumn[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: MappedColumn["User"] = relationship(back_populates="wallets")  # type: ignore
    transactions: MappedColumn[List["Transaction"]] = relationship(  # type: ignore
        back_populates="wallet"
    )
