from backend.src.core.modules.common.exceptions import PermissionDenied
from backend.src.core.modules.transaction.services.crud_service import (
    TransactionService,
)


class TransactionValidator:
    def __init__(self, transaction_service: TransactionService):
        self._transaction_service = transaction_service

    async def user_is_transaction_owner(
        self,
        user_id: int,
        transaction_id: int,
    ) -> None:
        transaction = await self._transaction_service.get_by_id(transaction_id)

        if user_id != transaction.user_id:
            raise PermissionDenied()
