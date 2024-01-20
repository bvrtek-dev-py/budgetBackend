from pydantic import BaseModel


class SubjectPayloadDTO(BaseModel):
    name: str

    class ConfigDict:
        frozen = True
