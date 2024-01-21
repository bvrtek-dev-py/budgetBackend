from datetime import datetime

from pydantic import BaseModel

from backend.src.core.modules.transaction.enum import TransactionType


class CategoryBaseResponse(BaseModel):
    id: int
    name: str
    transaction_type: TransactionType
    user_id: int

    class ConfigDict:
        frozen = True


class CategoryGetResponse(CategoryBaseResponse):
    created_at: datetime
    updated_at: datetime
