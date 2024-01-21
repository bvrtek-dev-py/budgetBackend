from datetime import datetime

from pydantic import BaseModel


class WalletBaseResponse(BaseModel):
    id: int
    name: str
    description: str
    user_id: int

    class ConfigDict:
        frozen = True


class WalletGetResponse(WalletBaseResponse):
    created_at: datetime
    updated_at: datetime
