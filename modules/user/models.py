from sqlalchemy import String
from sqlalchemy.orm import MappedColumn, mapped_column

from budgetBackend.database.base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    first_name: MappedColumn[str] = mapped_column(String(255))
    last_name: MappedColumn[str] = mapped_column(String(255))
    username: MappedColumn[str] = mapped_column(String(255), unique=True, index=True)
    email: MappedColumn[str] = mapped_column(String(255), unique=True)
    password: MappedColumn[str] = mapped_column(String(255))