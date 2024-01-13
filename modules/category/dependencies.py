from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.setup import get_session
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
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


async def _get_category_id(request: Request) -> int:
    """
    Extracts the subject_id from the query parameter or the request body.
    If value is in the query, it is returned
    If value is not in the query, it means that the dependency gets request
    """
    subject_id_from_query = request.path_params.get("category_id")
    if subject_id_from_query is not None:
        return int(subject_id_from_query)

    body = await request.json()
    return int(body["category_id"])


async def category_owner_permission(
    category_id: Annotated[int, Depends(_get_category_id)],
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    category_validator: Annotated[CategoryValidator, Depends(get_category_validator)],
):
    await category_validator.user_is_category_owner(current_user.id, category_id)
