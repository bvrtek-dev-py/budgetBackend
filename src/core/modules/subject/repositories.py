from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.src.core.modules.subject.interfaces import SubjectRepositoryInterface
from backend.src.core.modules.subject.models import Subject


class SubjectRepository(SubjectRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, subject: Subject) -> Subject:
        self._session.add(subject)
        await self._session.commit()

        return subject

    async def update(self, subject: Subject) -> Subject:
        await self._session.commit()
        await self._session.refresh(subject)

        return subject

    async def delete(self, subject: Subject) -> None:
        await self._session.delete(subject)
        await self._session.commit()

    async def get_by_user_id(self, user_id: int) -> Sequence[Subject]:
        result = await self._session.execute(
            select(Subject)
            .where(Subject.user_id == user_id)
            .options(selectinload(Subject.user))
        )

        return result.scalars().all()

    async def get_by_id(self, subject_id: int) -> Subject | None:
        result = await self._session.execute(
            select(Subject)
            .where(Subject.id == subject_id)
            .options(selectinload(Subject.user))
        )

        return result.scalars().first()

    async def get_by_name_and_user_id(self, name: str, user_id: int) -> Subject | None:
        result = await self._session.execute(
            select(Subject)
            .where((Subject.name == name) & (Subject.user_id == user_id))
            .options(selectinload(Subject.user))
        )

        return result.scalars().first()
