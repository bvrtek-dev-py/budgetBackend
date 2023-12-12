from pydantic import BaseModel

from backend.modules.category.enums import CategoryType


class CategoryBaseResponse(BaseModel):
    name: str
    type: CategoryType

    class ConfigDict:
        frozen = True
