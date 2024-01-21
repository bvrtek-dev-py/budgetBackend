from typing import Annotated

from fastapi import Depends, Request

from backend.src.dependencies.auth.permissions import get_current_user
from backend.src.dependencies.common.enums import IdentifierSource
from backend.src.dependencies.common.helpers import get_object_id
from backend.src.dependencies.subject.creators import get_subject_validator
from backend.src.core.modules.auth.schemas import CurrentUserDTO
from backend.src.core.modules.subject.validator import SubjectValidator


class SubjectOwnerPermission:
    def __init__(
        self,
        source: IdentifierSource = IdentifierSource.PATH_PARAMETER,
        identifier_name: str = "subject_id",
    ):
        self._source = source
        self._identifier_name = identifier_name

    async def __call__(
        self,
        request: Request,
        current_user: Annotated[CurrentUserDTO, Depends(get_current_user)],
        subject_validator: Annotated[SubjectValidator, Depends(get_subject_validator)],
    ):
        subject_id = await get_object_id(
            scope=self._source, request=request, name=self._identifier_name
        )

        await subject_validator.user_is_subject_owner(current_user.id, subject_id)
