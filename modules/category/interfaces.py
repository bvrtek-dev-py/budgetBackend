from abc import ABC, abstractmethod
from typing import Sequence

from backend.modules.category.models import Category
from backend.modules.transaction.enums import TransactionType


class CategoryRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def update(self, category: Category) -> Category:
        pass

    @abstractmethod
    async def delete(self, category: Category) -> None:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Sequence[Category]:
        pass

    @abstractmethod
    async def get_by_user_id_and_type(
        self, user_id: int, transaction_type: TransactionType
    ) -> Sequence[Category]:
        pass

    @abstractmethod
    async def get_by_id(self, category_id: int) -> Category | None:
        pass

    @abstractmethod
    async def get_by_name_and_user_id(self, name: str, user_id: int) -> Category | None:
        pass
