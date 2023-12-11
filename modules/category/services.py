from typing import Sequence

from budgetBackend.modules.category.enums import CategoryType
from budgetBackend.modules.category.models import Category
from budgetBackend.modules.category.repositories import CategoryRepository
from budgetBackend.modules.common.exceptions import ObjectDoesNotExist


class CategoryService:
    def __init__(self, repository: CategoryRepository):
        self._repository = repository

    async def create(
        self,
        name: str,
        category_type: CategoryType,
    ) -> Category:
        category = Category(
            name=name,
            type=category_type,
        )

        return await self._repository.save(category)

    async def update(self, category_id: int, name: str) -> Category:
        category = await self.get_by_id(category_id)

        category.name = name

        return await self._repository.update(category)

    async def delete(self, category_id: int) -> None:
        category = await self.get_by_id(category_id)

        return await self._repository.delete(category)

    async def get_by_id(self, category_id: int) -> Category:
        category = await self._repository.get_by_id(category_id)

        if category is None:
            raise ObjectDoesNotExist

        return category

    async def get_all(self) -> Sequence[Category]:
        return await self._repository.get_all()