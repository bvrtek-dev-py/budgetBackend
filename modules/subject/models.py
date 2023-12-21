from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import MappedColumn, mapped_column, relationship

from backend.database.base import BaseModel


class Subject(BaseModel):
    __tablename__ = "subjects"
    __table_args__ = (UniqueConstraint("name", "user_id", name="unique_user_name"),)

    name: MappedColumn[str] = mapped_column(String(50))
    user_id: MappedColumn[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: MappedColumn["User"] = relationship(back_populates="subjects")  # type: ignore
