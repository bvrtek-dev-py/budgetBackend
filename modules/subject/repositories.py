from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.subject.models import Subject


class SubjectRepository:
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

    async def get_all(self) -> Sequence[Subject]:
        result = await self._session.execute(select(Subject))

        return result.scalars().all()

    async def get_by_id(self, subject_id: int) -> Subject | None:
        return await self._session.get(Subject, subject_id)
