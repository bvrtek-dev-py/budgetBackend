from pydantic import BaseModel

from budgetBackend.modules.category.enums import CategoryType


class CategoryCreateRequest(BaseModel):
    name: str
    type: CategoryType

    class ConfigDict:
        frozen = True


class CategoryUpdateRequest(BaseModel):
    name: str

    class ConfigDict:
        frozen = True
