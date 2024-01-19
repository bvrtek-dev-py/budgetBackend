from typing import Annotated

from fastapi import Request, Depends

from backend.dependencies.auth.permissions import get_current_user
from backend.dependencies.category.creators import get_category_validator
from backend.dependencies.common.enums import IdentifierSource
from backend.dependencies.common.getters import get_object_id
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.category.validators import CategoryValidator


class CategoryOwnerPermission:
    def __init__(
        self,
        source: IdentifierSource,
        name: str = "category_id",
    ):
        """
        :param source - The source identifier of identifier (request or path parameter):
        :param name - The name of the identifier:
        """
        self._source = source
        self._name = name

    async def __call__(
        self,
        request: Request,
        current_user: Annotated[CurrentUserData, Depends(get_current_user)],
        category_validator: Annotated[
            CategoryValidator, Depends(get_category_validator)
        ],
    ) -> None:
        category_id = await get_object_id(
            scope=self._source, request=request, name=self._name
        )

        await category_validator.user_is_category_owner(current_user.id, category_id)
