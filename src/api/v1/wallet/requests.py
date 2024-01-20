from pydantic import BaseModel


class WalletCreateRequest(BaseModel):
    name: str
    description: str

    class ConfigDict:
        frozen = True


class WalletUpdateRequest(BaseModel):
    name: str
    description: str

    class ConfigDict:
        frozen = True
