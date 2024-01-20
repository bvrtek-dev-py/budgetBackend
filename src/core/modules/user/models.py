from typing import List

from sqlalchemy import String, Boolean
from sqlalchemy.orm import MappedColumn, mapped_column, relationship

from backend.src.database.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    first_name: MappedColumn[str] = mapped_column(String(255))
    last_name: MappedColumn[str] = mapped_column(String(255))
    username: MappedColumn[str] = mapped_column(String(255), unique=True, index=True)
    email: MappedColumn[str] = mapped_column(String(255), unique=True)
    password: MappedColumn[str] = mapped_column(String(255))
    is_admin: MappedColumn[bool] = mapped_column(Boolean, default=False)

    wallets: MappedColumn[List["Wallet"]] = relationship(back_populates="user")  # type: ignore
    categories: MappedColumn[List["Category"]] = relationship(back_populates="user")  # type: ignore
    subjects: MappedColumn[List["Subject"]] = relationship(back_populates="user")  # type: ignore
    transactions: MappedColumn[List["Transaction"]] = relationship(  # type: ignore
        back_populates="user"
    )
