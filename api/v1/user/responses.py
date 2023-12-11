from datetime import datetime

from pydantic import BaseModel


class UserBaseResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: str
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        frozen = True
