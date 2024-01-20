from pydantic import BaseModel, Field


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(min_length=6, max_length=20)
    password: str = Field(min_length=6, max_length=20)
    password_confirmation: str = Field(min_length=6, max_length=20)

    class ConfigDict:
        frozen = True
