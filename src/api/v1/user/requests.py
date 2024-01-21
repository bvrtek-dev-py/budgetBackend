from pydantic import BaseModel, Field, model_validator

from backend.src.core.modules.user.exceptions import PasswordDoesNotMatch


class UserBaseRequest(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    username: str = Field(min_length=3, max_length=20)

    class ConfigDict:
        frozen = True


class UserCreateRequest(UserBaseRequest):
    email: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=50)
    password_confirmation: str = Field(min_length=8, max_length=50)

    @model_validator(mode="after")
    def check_passwords_match(self) -> "UserCreateRequest":
        password1 = self.password
        password2 = self.password_confirmation

        if password1 is not None and password2 is not None and password1 != password2:
            raise PasswordDoesNotMatch()

        return self


class UserUpdateRequest(UserBaseRequest):
    pass
