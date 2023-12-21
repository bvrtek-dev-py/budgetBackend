from pydantic import BaseModel, Field


class SubjectRequest(BaseModel):
    name: str = Field(min_length=3, max_length=50)

    class ConfigDict:
        frozen = True
