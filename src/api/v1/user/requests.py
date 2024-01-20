from pydantic import BaseModel, Field, ValidationError


class UserCreateRequest(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    username: str = Field(min_length=3, max_length=20)
    email: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8, max_length=50)
    password_confirmation: str = Field(min_length=8, max_length=50)

    class ConfigDict:
        frozen = True

    @classmethod
    def validate_passwords_match(cls, values):
        if (
            "password" in values
            and "password_confirmation" in values
            and values["password"] != values["password_confirmation"]
        ):
            raise ValidationError("Passwords do not match")


class UserUpdateRequest(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    username: str = Field(min_length=3, max_length=20)

    class ConfigDict:
        frozen = True
