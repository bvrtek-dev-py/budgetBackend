from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.setup import get_session
from backend.src.dependencies.auth.creators import get_password_hash_service
from backend.src.core.modules.auth.services.password_services import PasswordHashService
from backend.src.core.modules.user.interfaces import UserRepositoryInterface
from backend.src.core.modules.user.repositories import UserRepository
from backend.src.core.modules.user.services import UserService
from backend.src.core.modules.user.use_cases import UserRetrievalUseCase


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> UserRepositoryInterface:
    return UserRepository(session)


def get_user_retrieval_use_case(
    repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)]
) -> UserRetrievalUseCase:
    return UserRetrievalUseCase(repository)


def get_user_service(
    repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
    retrieval_use_case: Annotated[
        UserRetrievalUseCase, Depends(get_user_retrieval_use_case)
    ],
    hash_service: Annotated[PasswordHashService, Depends(get_password_hash_service)],
) -> UserService:
    return UserService(
        repository=repository,
        retrieval_use_case=retrieval_use_case,
        password_hash_service=hash_service,
    )
