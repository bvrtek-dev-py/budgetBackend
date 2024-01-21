from datetime import datetime

from pydantic import BaseModel


class SubjectBaseResponse(BaseModel):
    id: int
    name: str

    class ConfigDict:
        frozen = True


class SubjectGetResponse(SubjectBaseResponse):
    user_id: int
    created_at: datetime
    updated_at: datetime
