from pydantic import BaseModel


class UserCreateRequest(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password1: str
    password2: str

    class ConfigDict:
        frozenset = True


class UserUpdateRequest(BaseModel):
    first_name: str
    last_name: str
    username: str

    class ConfigDict:
        frozenset = True
