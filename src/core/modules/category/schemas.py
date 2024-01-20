from pydantic import BaseModel

from backend.src.core.modules.transaction.enums import TransactionType


class CategoryCreateDTO(BaseModel):
    name: str
    transaction_type: TransactionType

    class ConfigDict:
        frozen = True


class CategoryUpdateDTO(BaseModel):
    name: str

    class ConfigDict:
        frozen = True
