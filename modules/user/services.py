from typing import Sequence, Optional

from backend.modules.auth.services import PasswordHashService
from backend.modules.common.exceptions import ObjectDoesNotExist, ObjectAlreadyExists
from backend.modules.user.exceptions import PasswordDoesNotMatch
from backend.modules.user.interfaces import UserRepositoryInterface
from backend.modules.user.models import User


class UserService:
    def __init__(
        self,
        repository: UserRepositoryInterface,
        password_hash_service: PasswordHashService,
    ):
        self._repository = repository
        self._password_hash_service = password_hash_service

    # pylint: disable=too-many-arguments
    async def create(
        self,
        username: str,
        email: str,
        first_name: str,
        last_name: str,
        password1: str,
        password2: str,
    ) -> User:
        if password1 != password2:
            raise PasswordDoesNotMatch()

        if await self._check_username_exists(username):
            raise ObjectAlreadyExists()

        if await self._check_email_exists(email):
            raise ObjectAlreadyExists()

        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=self._password_hash_service.hash(password1),
        )

        return await self._repository.save(user)

    async def update(
        self, user_id: int, username: str, first_name: str, last_name: str
    ) -> User:
        user = await self.get_by_id(user_id)

        if await self._check_username_exists(username, user_id):
            raise ObjectAlreadyExists()

        user.username = username
        user.first_name = first_name
        user.last_name = last_name

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
