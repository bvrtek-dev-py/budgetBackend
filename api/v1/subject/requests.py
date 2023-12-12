from pydantic import BaseModel


class SubjectCreateRequest(BaseModel):
    name: str

    class ConfigDict:
        frozen = True


class SubjectUpdateRequest(BaseModel):
    name: str

    class ConfigDict:
        frozen = True
