from pydantic import BaseModel


class ErrorResponse(BaseModel):
    detail: str

    class ConfigDict:
        frozen = True
