from pydantic import BaseModel, Field, model_validator

from backend.src.core.modules.user.exceptions import PasswordDoesNotMatch


class PasswordChangeRequest(BaseModel):
    current_password: str = Field(min_length=8, max_length=20)
    password: str = Field(min_length=8, max_length=20)
    password_confirmation: str = Field(min_length=8, max_length=20)

    @model_validator(mode="after")
    def check_passwords_match(self) -> "PasswordChangeRequest":
        password1 = self.password
        password2 = self.password_confirmation

        if password1 is not None and password2 is not None and password1 != password2:
            raise PasswordDoesNotMatch()

        return self

    class ConfigDict:
        frozen = True
