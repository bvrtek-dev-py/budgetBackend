from typing import Annotated

from fastapi import Depends

from backend.src.dependencies.auth.permissions import get_current_user
from backend.src.dependencies.user.creators import get_user_service
from backend.src.core.modules.auth.schemas import CurrentUserData
from backend.src.core.modules.common.exceptions import PermissionDenied
from backend.src.core.modules.user.services import UserService


async def admin_permission(
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> None:
    user = await user_service.get_by_id(current_user.id)

    if not user.is_admin:
        raise PermissionDenied()
