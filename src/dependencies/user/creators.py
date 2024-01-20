from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.setup import get_session
from backend.src.dependencies.auth.creators import get_password_hash_service
from backend.src.core.modules.auth.services import PasswordHashService
from backend.src.core.modules.user.interfaces import UserRepositoryInterface
from backend.src.core.modules.user.repositories import UserRepository
from backend.src.core.modules.user.services import UserService


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> UserRepositoryInterface:
    return UserRepository(session)


def get_user_service(
    repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
    hash_service: Annotated[PasswordHashService, Depends(get_password_hash_service)],
) -> UserService:
    return UserService(repository, hash_service)
