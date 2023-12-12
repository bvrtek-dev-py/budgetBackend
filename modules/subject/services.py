from typing import Sequence

from backend.modules.common.exceptions import ObjectDoesNotExist
from backend.modules.subject.models import Subject
from backend.modules.subject.repositories import SubjectRepository


class SubjectService:
    def __init__(self, repository: SubjectRepository):
        self._repository = repository

    async def create(self, name: str) -> Subject:
        subject = Subject(name=name)

        return await self._repository.save(subject)

    async def update(self, subject_id: int, name: str) -> Subject:
        subject = await self.get_by_id(subject_id)

        subject.name = name

        return await self._repository.update(subject)

    async def delete(self, subject_id: int):
        subject = await self.get_by_id(subject_id)

        return await self._repository.delete(subject)

    async def get_by_id(self, subject_id: int) -> Subject:
        subject = await self._repository.get_by_id(subject_id)

        if subject is None:
            raise ObjectDoesNotExist

        return subject

    async def get_all(self) -> Sequence[Subject]:
        return await self._repository.get_all()
