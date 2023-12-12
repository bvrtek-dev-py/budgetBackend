from sqlalchemy import String, Enum
from sqlalchemy.orm import MappedColumn, mapped_column

from backend.database.base import BaseModel
from backend.modules.category.enums import CategoryType


class Category(BaseModel):
    __tablename__ = "categories"

    name: MappedColumn[str] = mapped_column(String(50))
    type: MappedColumn[CategoryType] = mapped_column(
        Enum(
            CategoryType,
            create_constraint=True,
            validate_strings=True,
        )
    )
