from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.setup import get_session
from backend.modules.subject.interfaces import SubjectRepositoryInterface
from backend.modules.subject.repositories import SubjectRepository
from backend.modules.subject.services import SubjectService
from backend.modules.subject.validators import SubjectValidator


def get_subject_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> SubjectRepositoryInterface:
    return SubjectRepository(session)


def get_subject_service(
    repository: Annotated[SubjectRepositoryInterface, Depends(get_subject_repository)]
) -> SubjectService:
    return SubjectService(repository)


def get_subject_validator(
    service: Annotated[SubjectService, Depends(get_subject_service)]
) -> SubjectValidator:
    return SubjectValidator(service)
