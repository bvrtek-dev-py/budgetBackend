from pydantic import BaseModel, Field


class WalletBaseRequest(BaseModel):
    name: str = Field(min_length=2, max_length=20)
    description: str = Field(min_length=2, max_length=2000)

    class ConfigDict:
        frozen = True
