from pydantic import BaseModel, Field

from backend.src.core.modules.transaction.enum import TransactionType


class CategoryBaseRequest(BaseModel):
    name: str = Field(min_length=2, max_length=20)

    class ConfigDict:
        frozen = True


class CategoryCreateRequest(CategoryBaseRequest):
    transaction_type: TransactionType


class CategoryUpdateRequest(CategoryBaseRequest):
    pass
