from backend.src.core.modules.category.repository_interface import (
    CategoryRepositoryInterface,
)
from backend.src.core.modules.category.model import Category
from backend.src.core.modules.common.exceptions import ObjectDoesNotExist


class CategoryRetrievalUseCase:
    def __init__(self, repository: CategoryRepositoryInterface):
        self._repository = repository

    async def get_by_id(self, category_id: int) -> Category:
        category = await self._repository.get_by_id(category_id)

        if category is None:
            raise ObjectDoesNotExist()

        return category
