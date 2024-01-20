from pydantic import BaseModel


class WalletPayloadDTO(BaseModel):
    name: str
    description: str

    class ConfigDict:
        frozen = True
