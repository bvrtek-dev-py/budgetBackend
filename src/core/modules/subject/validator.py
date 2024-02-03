from backend.src.core.modules.common.exceptions import PermissionDenied
from backend.src.core.modules.subject.use_case import SubjectRetrievalUseCase


class SubjectValidator:
    def __init__(self, retrieval_use_case: SubjectRetrievalUseCase):
        self._retrieval_use_case = retrieval_use_case

    async def user_is_subject_owner(
        self,
        user_id: int,
        subject_id: int,
    ) -> None:
        subject = await self._retrieval_use_case.get_by_id(subject_id)

        if user_id != subject.user_id:
            raise PermissionDenied()
