from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from budgetBackend.database.setup import get_session
from budgetBackend.modules.category.repositories import CategoryRepository
from budgetBackend.modules.category.services import CategoryService


def get_category_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> CategoryRepository:
    return CategoryRepository(session)


def get_category_service(
    category_repository: Annotated[CategoryRepository, Depends(get_category_repository)]
) -> CategoryService:
    return CategoryService(category_repository)
