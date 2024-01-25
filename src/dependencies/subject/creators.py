from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.src.database.setup import get_session
from backend.src.core.modules.subject.repository_interface import (
    SubjectRepositoryInterface,
)
from backend.src.core.modules.subject.repository import SubjectRepository
from backend.src.core.modules.subject.service import SubjectService
from backend.src.core.modules.subject.validator import SubjectValidator


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