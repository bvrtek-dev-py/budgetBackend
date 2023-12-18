from datetime import datetime
from typing import List

from backend.api.v1.user.tests.data import base_user_data
from backend.modules.user.models import User


class InMemoryUserRepository:
    def __init__(self):
        self.users: List[User] = [
            User(
                id=1,
                first_name=base_user_data["first_name"],
                last_name=base_user_data["last_name"],
                username=base_user_data["username"],
                email=base_user_data["email"],
                password="1234",
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
        ]

    async def save(self, user: User) -> User:
        user.id = len(self.users) + 1
        self.users.append(user)

        return user

    async def update(self, user: User) -> User:
        return user

    async def delete(self, user: User) -> None:
        self.users.remove(user)

    async def get_all(self) -> List[User]:
        return self.users

    async def get_by_id(self, user_id: int) -> User | None:
        for user in self.users:
            if user.id == user_id:
                return user

        return None

    async def get_by_email(self, email: str) -> User | None:
        for user in self.users:
            if user.email == email:
                return user

        return None

    async def get_by_username(self, username: str) -> User | None:
        for user in self.users:
            if user.username == username:
                return user

        return None
