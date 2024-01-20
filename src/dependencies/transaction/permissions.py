from typing import Annotated

from fastapi import Depends, Request

from backend.src.dependencies.auth.permissions import get_current_user
from backend.src.dependencies.common.enums import IdentifierSource
from backend.src.dependencies.common.getters import get_object_id
from backend.src.dependencies.transaction.creators import get_transaction_validator
from backend.src.core.modules.auth.schemas import CurrentUserData
from backend.src.core.modules.transaction.validators import TransactionValidator


class TransactionOwnerPermission:
    def __init__(
        self,
        source: IdentifierSource = IdentifierSource.PATH_PARAMETER,
        name: str = "transaction_id",
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
        transaction_validator: Annotated[
            TransactionValidator, Depends(get_transaction_validator)
        ],
    ) -> None:
        wallet_id = await get_object_id(
            scope=self._source, request=request, name=self._name
        )

        await transaction_validator.user_is_transaction_owner(
            current_user.id, wallet_id
        )
