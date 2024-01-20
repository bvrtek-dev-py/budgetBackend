from typing import Sequence, Optional

from backend.src.core.modules.common.exceptions import (
    ObjectDoesNotExist,
    ObjectAlreadyExists,
)
from backend.src.core.modules.subject.interfaces import SubjectRepositoryInterface
from backend.src.core.modules.subject.models import Subject
from backend.src.core.modules.subject.schemas import SubjectPayloadDTO


class SubjectService:
    def __init__(self, repository: SubjectRepositoryInterface):
        self._repository = repository

    async def create(self, request_dto: SubjectPayloadDTO, user_id: int) -> Subject:
        if await self._check_subject_with_name_and_user_id_exists(
            request_dto.name, user_id
        ):
            raise ObjectAlreadyExists()

        subject = Subject(name=request_dto.name, user_id=user_id)

        return await self._repository.save(subject)

    async def update(self, subject_id: int, request_dto: SubjectPayloadDTO) -> Subject:
        subject = await self.get_by_id(subject_id)

        if await self._check_subject_with_name_and_user_id_exists(
            request_dto.name, subject.user_id, subject_id
        ):
            raise ObjectAlreadyExists()

        subject.name = request_dto.name

        return await self._repository.update(subject)

    async def delete(self, subject_id: int):
        subject = await self.get_by_id(subject_id)

        return await self._repository.delete(subject)

    async def get_by_id(self, subject_id: int) -> Subject:
        subject = await self._repository.get_by_id(subject_id)

        if subject is None:
            raise ObjectDoesNotExist()

        return subject

    async def get_by_user_id(self, user_id: int) -> Sequence[Subject]:
        return await self._repository.get_by_user_id(user_id)

    async def _check_subject_with_name_and_user_id_exists(
        self, name: str, user_id: int, exclude_id: Optional[int] = None
    ) -> bool:
        subject = await self._repository.get_by_name_and_user_id(name, user_id)

        if subject is None:
            return False

        if subject.id == exclude_id:
            return False

        return True
