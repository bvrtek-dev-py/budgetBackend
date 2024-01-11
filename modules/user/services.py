from typing import Sequence, Optional

from backend.modules.auth.services import PasswordHashService
from backend.modules.common.exceptions import ObjectDoesNotExist, ObjectAlreadyExists
from backend.modules.user.interfaces import UserRepositoryInterface
from backend.modules.user.models import User
from backend.modules.user.schemas import UserCreateDTO, UserUpdateDTO


class UserService:
    def __init__(
        self,
        repository: UserRepositoryInterface,
        password_hash_service: PasswordHashService,
    ):
        self._repository = repository
        self._password_hash_service = password_hash_service

    # pylint: disable=too-many-arguments
    async def create(self, request_dto: UserCreateDTO) -> User:
        if await self._check_username_exists(request_dto.username):
            raise ObjectAlreadyExists()

        if await self._check_email_exists(request_dto.email):
            raise ObjectAlreadyExists()

        password_hash = self._password_hash_service.hash(request_dto.password)
        user = User(**request_dto.model_dump() | {"password": password_hash})

        return await self._repository.save(user)

    async def update(self, user_id: int, request_dto: UserUpdateDTO) -> User:
        user = await self.get_by_id(user_id)

        if await self._check_username_exists(request_dto.username, user_id):
            raise ObjectAlreadyExists()

        for key, value in request_dto.model_dump().items():
            setattr(user, key, value)

        return await self._repository.update(user)

    async def delete(self, user_id: int):
        user = await self.get_by_id(user_id)

        return await self._repository.delete(user)

    async def get_by_id(self, user_id: int) -> User:
        user = await self._repository.get_by_id(user_id)

        if user is None:
            raise ObjectDoesNotExist()

        return user

    async def get_by_email(self, email: str) -> User:
        user = await self._repository.get_by_email(email)

        if user is None:
            raise ObjectDoesNotExist()

        return user

    async def get_by_username_or_email(self, field: str) -> User:
        user = await self._repository.get_by_email(field)
        if user is not None:
            return user

        user = await self._repository.get_by_username(field)
        if user is not None:
            return user

        raise ObjectDoesNotExist()

    async def _check_username_exists(
        self, username: str, excluded_id: Optional[int] = None
    ) -> bool:
        user = await self._repository.get_by_username(username)

        if user is None:
            return False

        if user.id == excluded_id:
            return False

        return True

    async def _check_email_exists(
        self, email: str, excluded_id: Optional[int] = None
    ) -> bool:
        user = await self._repository.get_by_email(email)

        if user is None:
            return False

        if user.id == excluded_id:
            return False

        return True

    async def get_all(self) -> Sequence[User]:
        return await self._repository.get_all()
