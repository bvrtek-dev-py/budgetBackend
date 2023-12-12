from sqlalchemy import String
from sqlalchemy.orm import MappedColumn, mapped_column

from backend.database.base import BaseModel


class Subject(BaseModel):
    __tablename__ = "subjects"

    name: MappedColumn[str] = mapped_column(String(50))
