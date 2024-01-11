from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

    class ConfigDict:
        frozen = True


class UserUpdateDTO(BaseModel):
    first_name: str
    last_name: str
    username: str

    class ConfigDict:
        frozen = True
