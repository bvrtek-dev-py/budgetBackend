from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.setup import get_session
from backend.src.core.modules.category.interfaces import CategoryRepositoryInterface
from backend.src.core.modules.category.repositories import CategoryRepository
from backend.src.core.modules.category.services import CategoryService
from backend.src.core.modules.category.validators import CategoryValidator


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
