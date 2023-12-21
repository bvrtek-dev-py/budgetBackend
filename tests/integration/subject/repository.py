from datetime import datetime
from typing import List

from backend.modules.subject.interfaces import SubjectRepositoryInterface
from backend.modules.subject.models import Subject
from backend.tests.integration.subject.data import get_subject_data


class InMemorySubjectRepository(SubjectRepositoryInterface):
    def __init__(self):
        self._subjects: List[Subject] = get_subject_data()

    async def save(self, subject: Subject) -> Subject:
        subject.id = len(self._subjects) + 1
        subject.created_at = subject.updated_at = datetime.utcnow()
        self._subjects.append(subject)

        return subject

    async def update(self, subject: Subject) -> Subject:
        return subject

    async def delete(self, subject: Subject) -> None:
        self._subjects.remove(subject)

    async def get_by_user_id(self, user_id: int) -> List[Subject]:
        return [subject for subject in self._subjects if subject.user_id == user_id]

    async def get_by_id(self, subject_id: int) -> Subject | None:
        for subject in self._subjects:
            if subject.id == subject_id:
                return subject

        return None

    async def get_by_name_and_user_id(self, name: str, user_id: int) -> Subject | None:
        for subject in self._subjects:
            if subject.name == name and subject.user_id == user_id:
                return subject

        return None
