from typing import Sequence, Optional

from backend.src.core.modules.auth.services.password_services import PasswordHashService
from backend.src.core.modules.common.exceptions import (
    ObjectAlreadyExists,
)
from backend.src.core.modules.user.interfaces import UserRepositoryInterface
from backend.src.core.modules.user.models import User
from backend.src.core.modules.user.schemas import UserCreateDTO, UserUpdateDTO
from backend.src.core.modules.user.use_cases import UserRetrievalUseCase


class UserService:
    def __init__(
        self,
        repository: UserRepositoryInterface,
        retrieval_use_case: UserRetrievalUseCase,
        password_hash_service: PasswordHashService,
    ):
        self._repository = repository
        self._retrieval_use_case = retrieval_use_case
        self._password_hash_service = password_hash_service

    async def create(self, request_dto: UserCreateDTO) -> User:
        if await self._check_user_with_username_exists(request_dto.username):
            raise ObjectAlreadyExists()

        if await self._check_user_with_email_exists(request_dto.email):
            raise ObjectAlreadyExists()

        password_hash = self._password_hash_service.hash(request_dto.password)
        user = User(**request_dto.model_dump() | {"password": password_hash})

        return await self._repository.save(user)

    async def update(self, user_id: int, request_dto: UserUpdateDTO) -> User:
        user = await self.get_by_id(user_id)

        if await self._check_user_with_username_exists(request_dto.username, user_id):
            raise ObjectAlreadyExists()

        for key, value in request_dto.model_dump().items():
            setattr(user, key, value)

        return await self._repository.update(user)

    async def delete(self, user_id: int):
        user = await self.get_by_id(user_id)

        return await self._repository.delete(user)

    async def get_all(self) -> Sequence[User]:
        return await self._repository.get_all()

    async def get_by_id(self, user_id: int) -> User:
        return await self._retrieval_use_case.get_by_id(user_id)

    async def _check_user_with_username_exists(
        self, username: str, excluded_id: Optional[int] = None
    ) -> bool:
        user = await self._repository.get_by_username(username)

        if user is None:
            return False

        if user.id == excluded_id:
            return False

        return True

    async def _check_user_with_email_exists(
        self, email: str, excluded_id: Optional[int] = None
    ) -> bool:
        user = await self._repository.get_by_email(email)

        if user is None:
            return False

        if user.id == excluded_id:
            return False

        return True
