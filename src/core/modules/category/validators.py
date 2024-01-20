from backend.src.core.modules.category.services import CategoryService
from backend.src.core.modules.common.exceptions import PermissionDenied


class CategoryValidator:
    def __init__(self, subject_service: CategoryService):
        self._category_service = subject_service

    async def user_is_category_owner(
        self,
        user_id: int,
        subject_id: int,
    ) -> None:
        category = await self._category_service.get_by_id(subject_id)

        if user_id != category.user_id:
            raise PermissionDenied()
