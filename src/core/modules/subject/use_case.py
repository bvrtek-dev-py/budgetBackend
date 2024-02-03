from backend.src.core.modules.subject.repository_interface import (
    SubjectRepositoryInterface,
)
from backend.src.core.modules.common.exceptions import ObjectDoesNotExist
from backend.src.core.modules.subject.model import Subject


class SubjectRetrievalUseCase:
    def __init__(self, repository: SubjectRepositoryInterface):
        self._repository = repository

    async def get_by_id(self, subject_id: int) -> Subject:
        subject = await self._repository.get_by_id(subject_id)

        if subject is None:
            raise ObjectDoesNotExist()

        return subject
