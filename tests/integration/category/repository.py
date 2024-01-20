from datetime import datetime
from typing import List

from backend.src.core.modules.category.interfaces import CategoryRepositoryInterface
from backend.src.core.modules.category.models import Category
from backend.src.core.modules.transaction.enums import TransactionType
from backend.tests.database import get_category_data


class InMemoryCategoryRepository(CategoryRepositoryInterface):
    def __init__(self):
        self._categories: List[Category] = get_category_data()

    async def save(self, category: Category) -> Category:
        category.id = len(self._categories) + 1
        category.created_at = category.updated_at = datetime.utcnow()
        self._categories.append(category)
        return category

    async def update(self, category: Category) -> Category:
        return category

    async def delete(self, category: Category) -> None:
        self._categories.remove(category)

    async def get_by_user_id(self, user_id: int) -> List[Category]:
        return [
            category for category in self._categories if category.user_id == user_id
        ]

    async def get_by_user_id_and_type(
        self, user_id: int, transaction_type: TransactionType
    ) -> List[Category]:
        return [
            category
            for category in self._categories
            if category.user_id == user_id
            and category.transaction_type == transaction_type
        ]

    async def get_by_id(self, category_id: int) -> Category | None:
        for category in self._categories:
            if category.id == category_id:
                return category
        return None

    async def get_by_name_and_user_id(self, name: str, user_id: int) -> Category | None:
        for category in self._categories:
            if category.name == name and category.user_id == user_id:
                return category
        return None
