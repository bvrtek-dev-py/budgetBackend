# pylint: disable=R0801
from abc import ABC, abstractmethod
from typing import Sequence

from backend.modules.user.models import User


class UserRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete(self, user: User) -> None:
        pass

    @abstractmethod
    async def get_all(self) -> Sequence[User]:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None:
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> User | None:
        pass
