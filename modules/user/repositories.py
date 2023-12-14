from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, user: User) -> User:
        self._session.add(user)
        await self._session.commit()

        return user

    async def update(self, user: User) -> User:
        await self._session.commit()
        await self._session.refresh(user)

        return user

    async def delete(self, user: User) -> None:
        await self._session.delete(user)
        await self._session.commit()

    async def get_all(self) -> Sequence[User]:
        result = await self._session.execute(select(User))

        return result.scalars().all()

    async def get_by_id(self, user_id: int) -> User | None:
        return await self._session.get(User, user_id)

    async def get_by_email(self, email: str) -> User | None:
        result = await self._session.execute(select(User).where(User.email == email))
        return result.scalars().first()

    async def get_by_username(self, username: str) -> User | None:
        result = await self._session.execute(
            select(User).where(User.username == username)
        )
        return result.scalars().first()
