from datetime import datetime

from sqlalchemy import Integer, DateTime, func
from sqlalchemy.orm import MappedColumn, mapped_column
from sqlalchemy.orm import declarative_base


class Base:
    id: MappedColumn[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: MappedColumn[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: MappedColumn[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )


BaseModel = declarative_base(cls=Base)
