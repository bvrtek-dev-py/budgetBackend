from pydantic import BaseModel

from backend.src.core.modules.transaction.enums import TransactionType


class CategoryBaseDTO(BaseModel):
    name: str

    class ConfigDict:
        frozen = True


class CategoryCreateDTO(CategoryBaseDTO):
    transaction_type: TransactionType


class CategoryUpdateDTO(CategoryBaseDTO):
    pass
