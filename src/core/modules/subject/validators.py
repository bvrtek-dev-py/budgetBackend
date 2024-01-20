from backend.src.core.modules.common.exceptions import PermissionDenied
from backend.src.core.modules.subject.services import SubjectService


class SubjectValidator:
    def __init__(self, subject_service: SubjectService):
        self._subject_service = subject_service

    async def user_is_subject_owner(
        self,
        user_id: int,
        subject_id: int,
    ) -> None:
        subject = await self._subject_service.get_by_id(subject_id)

        if user_id != subject.user_id:
            raise PermissionDenied()
