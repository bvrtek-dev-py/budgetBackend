from backend.modules.transaction.enums import TransactionType
from backend.modules.transaction.interfaces import TransactionRepositoryInterface
from backend.modules.transaction.models import Transaction
from backend.modules.transaction.schemas.transaction import TransactionTransferDTO


class TransactionTransferService:
    def __init__(self, repository: TransactionRepositoryInterface):
        self._repository = repository

    async def transfer(
        self,
        sender_id: int,
        receiver_id: int,
        user_id: int,
        request_dto: TransactionTransferDTO,
    ) -> TransactionTransferDTO:
        await self._make_transaction(
            sender_id, user_id, TransactionType.EXPENSE, request_dto
        )
        await self._make_transaction(
            receiver_id, user_id, TransactionType.INCOME, request_dto
        )

        return request_dto

    async def _make_transaction(
        self,
        wallet_id: int,
        user_id: int,
        transaction_type: TransactionType,
        request_dto: TransactionTransferDTO,
    ) -> Transaction:
        transaction = Transaction(
            **request_dto.model_dump(),
            wallet_id=wallet_id,
            user_id=user_id,
            type=transaction_type,
            is_transfer=True
        )

        return await self._repository.save(transaction)
