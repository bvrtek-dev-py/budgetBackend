from pydantic import BaseModel

from backend.src.core.modules.transaction.enums import TransactionType


class CategoryCreateRequest(BaseModel):
    name: str
    transaction_type: TransactionType

    class ConfigDict:
        frozen = True


class CategoryUpdateRequest(BaseModel):
    name: str

    class ConfigDict:
        frozen = True
