from typing import List

from backend.modules.user.interfaces import UserRepositoryInterface
from backend.modules.user.models import User
from backend.tests.integration.user.data import get_user_db


class InMemoryUserRepository(UserRepositoryInterface):
    def __init__(self):
        self._users: List[User] = get_user_db()

    async def save(self, user: User) -> User:
        user.id = len(self._users) + 1
        self._users.append(user)

        return user

    async def update(self, user: User) -> User:
        return user

    async def delete(self, user: User) -> None:
        self._users.remove(user)

    async def get_all(self) -> List[User]:
        return self._users

    async def get_by_id(self, user_id: int) -> User | None:
        for user in self._users:
            if user.id == user_id:
                return user

        return None

    async def get_by_email(self, email: str) -> User | None:
        for user in self._users:
            if user.email == email:
                return user

        return None

    async def get_by_username(self, username: str) -> User | None:
        for user in self._users:
            if user.username == username:
                return user

        return None
