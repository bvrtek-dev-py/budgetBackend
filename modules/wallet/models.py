from sqlalchemy import String, Text
from sqlalchemy.orm import MappedColumn, mapped_column

from budgetBackend.database.base import BaseModel


class Wallet(BaseModel):
    __tablename__ = "wallets"

    name: MappedColumn[str] = mapped_column(String(50))
    description: MappedColumn[str] = mapped_column(Text(2000), default="")
