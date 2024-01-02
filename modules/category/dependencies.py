from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.setup import get_session
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.category.interfaces import CategoryRepositoryInterface
from backend.modules.category.repositories import CategoryRepository
from backend.modules.category.services import CategoryService
from backend.modules.common.exceptions import PermissionDenied


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


def _get_category_id(category_id: int = Path(...)) -> int:
    return category_id


async def category_owner_permission(
    category_id: Annotated[int, Depends(_get_category_id)],
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    category = await category_service.get_by_id(category_id)

    if category.user_id != current_user.id:
        raise PermissionDenied()
