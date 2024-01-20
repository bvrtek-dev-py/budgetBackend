from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.src.core.modules.category.interfaces import CategoryRepositoryInterface
from backend.src.core.modules.category.models import Category
from backend.src.core.modules.transaction.enums import TransactionType


class CategoryRepository(CategoryRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, category: Category) -> Category:
        self._session.add(category)
        await self._session.commit()

        return category

    async def update(self, category: Category) -> Category:
        await self._session.commit()
        await self._session.refresh(category)

        return category

    async def delete(self, category: Category) -> None:
        await self._session.delete(category)
        await self._session.commit()

    async def get_by_user_id(self, user_id: int) -> Sequence[Category]:
        result = await self._session.execute(
            select(Category)
            .where(Category.user_id == user_id)
            .options(selectinload(Category.user))
        )

        return result.scalars().all()

    async def get_by_user_id_and_type(
        self, user_id: int, transaction_type: TransactionType
    ) -> Sequence[Category]:
        result = await self._session.execute(
            select(Category)
            .where(
                (Category.user_id == user_id)
                & (Category.transaction_type == transaction_type)
            )
            .options(selectinload(Category.user))
        )

        return result.scalars().all()

    async def get_by_id(self, category_id: int) -> Category | None:
        result = await self._session.execute(
            select(Category)
            .where(Category.id == category_id)
            .options(selectinload(Category.user))
        )

        return result.scalars().first()

    async def get_by_name_and_user_id(self, name: str, user_id: int) -> Category | None:
        result = await self._session.execute(
            select(Category)
            .where((Category.name == name) & (Category.user_id == user_id))
            .options(selectinload(Category.user))
        )

        return result.scalars().first()
