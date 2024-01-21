from datetime import datetime

from pydantic import BaseModel


class AuthenticatedUserDTO(BaseModel):
    id: int
    sub: str

    class ConfigDict:
        frozen = True


class CurrentUserDTO(BaseModel):
    id: int
    email: str

    class ConfigDict:
        frozen = True


class ChangePasswordDTO(BaseModel):
    current_password: str
    password: str
    password_confirmation: str

    class ConfigDict:
        frozen = True


class SuccessAuthenticationDTO(BaseModel):
    token_type: str
    access_token: str
    refresh_token: str
    expired_at: datetime

    class ConfigDict:
        frozen = True
