from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.setup import get_session
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.common.exceptions import PermissionDenied
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


def _get_subject_id(subject_id: int = Path(...)) -> int:
    return subject_id


async def subject_owner_permission(
    subject_id: Annotated[int, Depends(_get_subject_id)],
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    subject_validator: Annotated[SubjectValidator, Depends(get_subject_validator)],
):
    if (
        await subject_validator.user_is_subject_owner(current_user.id, subject_id)
        is False
    ):
        raise PermissionDenied()
