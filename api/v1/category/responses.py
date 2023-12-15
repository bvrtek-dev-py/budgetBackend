from pydantic import BaseModel

from backend.modules.transaction.enums import TransactionType


class CategoryBaseResponse(BaseModel):
    name: str
    transaction_type: TransactionType

    class ConfigDict:
        frozen = True
