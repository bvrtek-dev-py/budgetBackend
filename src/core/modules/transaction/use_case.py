from backend.src.core.modules.common.exceptions import ObjectDoesNotExist
from backend.src.core.modules.transaction.model import Transaction
from backend.src.core.modules.transaction.repository import TransactionRepository


class TransactionRetrievalUseCase:
    def __init__(self, repository: TransactionRepository):
        self._repository = repository

    async def get_by_id(self, transaction_id: int) -> Transaction:
        transaction = await self._repository.get_by_id(transaction_id)

        if transaction is None:
            raise ObjectDoesNotExist()

        return transaction
