from backend.src.core.modules.common.exceptions import PermissionDenied
from backend.src.core.modules.transaction.use_case import TransactionRetrievalUseCase


class TransactionValidator:
    def __init__(self, retrieval_use_case: TransactionRetrievalUseCase):
        self._retrieval_use_case = retrieval_use_case

    async def user_is_transaction_owner(
        self,
        user_id: int,
        transaction_id: int,
    ) -> None:
        transaction = await self._retrieval_use_case.get_by_id(transaction_id)

        if user_id != transaction.user_id:
            raise PermissionDenied()
