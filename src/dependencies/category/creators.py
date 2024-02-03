from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.setup import get_session
from backend.src.core.modules.category.repository_interface import (
    CategoryRepositoryInterface,
)
from backend.src.core.modules.category.repository import CategoryRepository
from backend.src.core.modules.category.service import CategoryService
from backend.src.core.modules.category.validator import CategoryValidator
from backend.src.core.modules.category.use_case import CategoryRetrievalUseCase


def get_category_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> CategoryRepositoryInterface:
    return CategoryRepository(session)


def get_category_retrieval_use_case(
    repository: Annotated[CategoryRepositoryInterface, Depends(get_category_repository)]
) -> CategoryRetrievalUseCase:
    return CategoryRetrievalUseCase(repository)


def get_category_service(
    repository: Annotated[
        CategoryRepositoryInterface, Depends(get_category_repository)
    ],
    retrieval_use_case: Annotated[
        CategoryRetrievalUseCase, Depends(get_category_retrieval_use_case)
    ],
) -> CategoryService:
    return CategoryService(repository=repository, retrieval_use_case=retrieval_use_case)


def get_category_validator(
    retrieval_use_case: Annotated[
        CategoryRetrievalUseCase, Depends(get_category_service)
    ]
) -> CategoryValidator:
    return CategoryValidator(retrieval_use_case)
