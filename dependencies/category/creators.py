from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.setup import get_session
from backend.modules.category.interfaces import CategoryRepositoryInterface
from backend.modules.category.repositories import CategoryRepository
from backend.modules.category.services import CategoryService
from backend.modules.category.validators import CategoryValidator


def get_category_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> CategoryRepositoryInterface:
    return CategoryRepository(session)


def get_category_service(
    category_repository: Annotated[
        CategoryRepositoryInterface, Depends(get_category_repository)
    ]
) -> CategoryService:
    return CategoryService(category_repository)


def get_category_validator(
    category_service: Annotated[CategoryService, Depends(get_category_service)]
) -> CategoryValidator:
    return CategoryValidator(category_service)
