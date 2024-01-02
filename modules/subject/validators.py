from backend.modules.subject.services import SubjectService


class SubjectValidator:
    def __init__(self, subject_service: SubjectService):
        self._subject_service = subject_service

    async def user_is_subject_owner(
        self,
        user_id: int,
        subject_id: int,
    ) -> bool:
        subject = await self._subject_service.get_by_id(subject_id)
        return user_id == subject.user_id
