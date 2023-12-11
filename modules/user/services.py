from typing import Sequence

from budgetBackend.modules.common.exceptions import ObjectDoesNotExist
from budgetBackend.modules.user.exceptions import PasswordDoesNotMatch
from budgetBackend.modules.user.models import User
from budgetBackend.modules.user.repositories import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self._repository = repository

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
            raise PasswordDoesNotMatch

        user = User( # TODO add factory
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password1,
        )

        return await self._repository.save(user)

    async def update(
        self, user_id: int, username: str, first_name: str, last_name: str
    ) -> User:
        user = await self.get_by_id(user_id)

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
            raise ObjectDoesNotExist

        return user

    async def get_all(self) -> Sequence[User]:
        return await self._repository.get_all()
