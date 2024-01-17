from typing import Annotated

from fastapi import Depends, Path

from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.dependencies.transaction.creators import get_transaction_validator
from backend.modules.transaction.validators import TransactionValidator


def _get_transaction_id(transaction_id: int = Path(...)) -> int:
    return transaction_id


async def transaction_owner_permission(
    transaction_id: Annotated[int, Depends(_get_transaction_id)],
    current_user: Annotated[CurrentUserData, Depends(get_current_user)],
    transaction_validator: Annotated[
        TransactionValidator, Depends(get_transaction_validator)
    ],
):
    await transaction_validator.user_is_transaction_owner(
        current_user.id, transaction_id
    )
