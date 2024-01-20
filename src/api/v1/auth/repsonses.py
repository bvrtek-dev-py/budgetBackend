from datetime import datetime

from pydantic import BaseModel


class LoginSuccessResponse(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
    expired_at: datetime

    class ConfigDict:
        frozen = True
