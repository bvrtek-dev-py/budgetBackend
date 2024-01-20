from abc import ABC, abstractmethod
from typing import Sequence

from backend.src.core.modules.subject.models import Subject


class SubjectRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, subject: Subject) -> Subject:
        pass

    @abstractmethod
    async def update(self, subject: Subject) -> Subject:
        pass

    @abstractmethod
    async def delete(self, subject: Subject) -> None:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Sequence[Subject]:
        pass

    @abstractmethod
    async def get_by_id(self, subject_id: int) -> Subject | None:
        pass

    @abstractmethod
    async def get_by_name_and_user_id(self, name: str, user_id: int) -> Subject | None:
        pass
