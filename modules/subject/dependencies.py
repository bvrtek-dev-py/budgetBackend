from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from budgetBackend.database.setup import get_session
from budgetBackend.modules.subject.repositories import SubjectRepository
from budgetBackend.modules.subject.services import SubjectService


def get_subject_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> SubjectRepository:
    return SubjectRepository(session)


def get_subject_service(
    repository: Annotated[SubjectRepository, Depends(get_subject_repository)]
) -> SubjectService:
    return SubjectService(repository)
