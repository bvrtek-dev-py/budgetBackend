from datetime import datetime

from pydantic import BaseModel


class WalletBaseResponse(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        frozen = True
