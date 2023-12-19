from pydantic import BaseModel, Field


class UserCreateRequest(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    username: str = Field(min_length=3, max_length=20)
    email: str = Field(min_length=3, max_length=50)
    password1: str = Field(min_length=8, max_length=50)
    password2: str = Field(min_length=8, max_length=50)

    class ConfigDict:
        frozen = True


class UserUpdateRequest(BaseModel):
    first_name: str = Field(min_length=3, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    username: str = Field(min_length=3, max_length=20)

    class ConfigDict:
        frozen = True
