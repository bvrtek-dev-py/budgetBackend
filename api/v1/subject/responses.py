from datetime import datetime

from pydantic import BaseModel


class SubjectBaseResponse(BaseModel):
    id: int
    name: str
    created_at: datetime
    updated_at: datetime

    class ConfigDict:
        frozen = True
