from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.setup import get_session
from backend.modules.auth.dependencies import get_password_hash_service
from backend.modules.auth.services import PasswordHashService
from backend.modules.user.interfaces import UserRepositoryInterface
from backend.modules.user.repositories import UserRepository
from backend.modules.user.services import UserService


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> UserRepositoryInterface:
    return UserRepository(session)


def get_user_service(
    repository: Annotated[UserRepositoryInterface, Depends(get_user_repository)],
    hash_service: Annotated[PasswordHashService, Depends(get_password_hash_service)],
) -> UserService:
    return UserService(repository, hash_service)
