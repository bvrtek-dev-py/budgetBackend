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
from backend.src.core.modules.subject.use_case import SubjectRetrievalUseCase


def get_subject_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> SubjectRepositoryInterface:
    return SubjectRepository(session)


def get_subject_retrieval_use_case(
    repository: Annotated[SubjectRepositoryInterface, Depends(get_subject_repository)]
) -> SubjectRetrievalUseCase:
    return SubjectRetrievalUseCase(repository)


def get_subject_service(
    repository: Annotated[SubjectRepositoryInterface, Depends(get_subject_repository)],
    retrieval_use_case: Annotated[
        SubjectRetrievalUseCase, Depends(get_subject_retrieval_use_case)
    ],
) -> SubjectService:
    return SubjectService(repository=repository, retrieval_use_case=retrieval_use_case)


def get_subject_validator(
    retrieval_use_case: Annotated[
        SubjectRetrievalUseCase, Depends(get_subject_retrieval_use_case)
    ]
) -> SubjectValidator:
    return SubjectValidator(retrieval_use_case)
