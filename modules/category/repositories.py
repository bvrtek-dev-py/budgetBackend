from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.category.models import Category


class CategoryRepository:
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

    async def get_all(self) -> Sequence[Category]:
        result = await self._session.execute(select(Category))

        return result.scalars().all()

    async def get_by_id(self, category_id: int) -> Category | None:
        return await self._session.get(Category, category_id)
