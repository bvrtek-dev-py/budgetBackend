from datetime import datetime

from pydantic import BaseModel, Field


class WalletBaseResponse(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=2000)
    user_id: int

    class ConfigDict:
        frozen = True
        orm_mode = True


class WalletGetResponse(WalletBaseResponse):
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        frozen = True
        orm_mode = True
