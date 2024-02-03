from backend.src.core.modules.category.use_case import CategoryRetrievalUseCase
from backend.src.core.modules.common.exceptions import PermissionDenied


class CategoryValidator:
    def __init__(self, retrieval_use_case: CategoryRetrievalUseCase):
        self._retrieval_use_case = retrieval_use_case

    async def user_is_category_owner(
        self,
        user_id: int,
        subject_id: int,
    ) -> None:
        category = await self._retrieval_use_case.get_by_id(subject_id)

        if user_id != category.user_id:
            raise PermissionDenied()
