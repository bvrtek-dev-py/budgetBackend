from pydantic import BaseModel


class UserBaseDTO(BaseModel):
    first_name: str
    last_name: str
    username: str

    class ConfigDict:
        frozen = True


class UserCreateDTO(UserBaseDTO):
    email: str
    password: str

    class ConfigDict:
        frozen = True


class UserUpdateDTO(UserBaseDTO):
    pass
