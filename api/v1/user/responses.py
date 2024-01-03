from decimal import Decimal

from pydantic import BaseModel


class UserBaseResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str

    class ConfigDict:
        frozen = True
        orm_mode = True


class UserBalanceResponse(BaseModel):
    id: int
    balance: Decimal

    class ConfigDict:
        frozen = True
