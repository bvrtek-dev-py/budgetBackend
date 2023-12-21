from typing import Annotated

from fastapi import Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.setup import get_session
from backend.modules.auth.dependencies import get_current_user
from backend.modules.common.exceptions import PermissionDenied
from backend.modules.subject.repositories import SubjectRepository
from backend.modules.subject.services import SubjectService


def get_subject_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> SubjectRepository:
    return SubjectRepository(session)


def get_subject_service(
    repository: Annotated[SubjectRepository, Depends(get_subject_repository)]
) -> SubjectService:
    return SubjectService(repository)


def _get_subject_id(subject_id: int = Path(...)) -> int:
    return subject_id


async def subject_owner_permission(
    subject_id: Annotated[int, Depends(_get_subject_id)],
    current_user_email: Annotated[str, Depends(get_current_user)],
    wallet_service: Annotated[SubjectService, Depends(get_subject_service)],
):
    subject = await wallet_service.get_by_id(subject_id)

    if subject.user.email != current_user_email:
        raise PermissionDenied
