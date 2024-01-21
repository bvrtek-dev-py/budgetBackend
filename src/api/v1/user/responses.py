from pydantic import BaseModel


class UserBaseResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str

    class ConfigDict:
        frozen = True
