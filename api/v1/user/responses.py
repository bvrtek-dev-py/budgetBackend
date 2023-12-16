from typing import List

from pydantic import BaseModel

from backend.api.v1.wallet.responses import WalletBaseResponse


class UserBaseResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    wallets: List[WalletBaseResponse]

    class ConfigDict:
        frozen = True
        orm_mode = True
