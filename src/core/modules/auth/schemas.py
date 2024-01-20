from pydantic import BaseModel


class TokenData(BaseModel):
    user_id: int
    sub: str

    class ConfigDict:
        frozen = True


class CurrentUserData(BaseModel):
    id: int
    email: str

    class ConfigDict:
        frozen = True


class ChangePasswordDTO(BaseModel):
    current_password: str
    password: str
    password_confirmation: str
