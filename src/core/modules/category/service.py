from typing import Sequence, Optional

from backend.src.core.modules.category.model import Category
from backend.src.core.modules.category.repository_interface import (
    CategoryRepositoryInterface,
)
from backend.src.core.modules.category.schemas import (
    CategoryCreateDTO,
    CategoryUpdateDTO,
)
from backend.src.core.modules.category.use_case import CategoryRetrievalUseCase
from backend.src.core.modules.common.exceptions import (
    ObjectAlreadyExists,
)
from backend.src.core.modules.transaction.enum import TransactionType


class CategoryService:
    def __init__(
        self,
        repository: CategoryRepositoryInterface,
        retrieval_use_case: CategoryRetrievalUseCase,
    ):
        self._repository = repository
        self._retrieval_use_case = retrieval_use_case

    async def create(self, user_id: int, request_dto: CategoryCreateDTO) -> Category:
        if await self._check_category_with_name_and_user_id_exists(
            request_dto.name, user_id
        ):
            raise ObjectAlreadyExists()

        category = Category(**request_dto.model_dump(), user_id=user_id)

        return await self._repository.save(category)

    async def update(
        self, category_id: int, request_dto: CategoryUpdateDTO
    ) -> Category:
        category = await self.get_by_id(category_id)

        if await self._check_category_with_name_and_user_id_exists(
            request_dto.name, category.user_id, category.id
        ):
            raise ObjectAlreadyExists()

        category.name = request_dto.name

        return await self._repository.update(category)

    async def delete(self, category_id: int) -> None:
        category = await self.get_by_id(category_id)

        return await self._repository.delete(category)

    async def get_by_id(self, category_id: int) -> Category:
        return await self._retrieval_use_case.get_by_id(category_id)

    async def get_by_user_id(
        self, user_id: int, transaction_type: Optional[TransactionType] = None
    ) -> Sequence[Category]:
        if transaction_type is not None:
            return await self._repository.get_by_user_id_and_type(
                user_id, transaction_type
            )

        return await self._repository.get_by_user_id(user_id)

    async def _check_category_with_name_and_user_id_exists(
        self, name: str, user_id: int, exclude_id: Optional[int] = None
    ) -> bool:
        category = await self._repository.get_by_name_and_user_id(name, user_id)

        if category is None:
            return False

        if category.id == exclude_id:
            return False

        return True
