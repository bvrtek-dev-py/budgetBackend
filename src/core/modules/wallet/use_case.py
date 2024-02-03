from backend.src.core.modules.wallet.repository_interface import (
    WalletRepositoryInterface,
)
from backend.src.core.modules.common.exceptions import ObjectDoesNotExist
from backend.src.core.modules.wallet.model import Wallet


class WalletRetrievalUseCase:
    def __init__(self, repository: WalletRepositoryInterface):
        self._repository = repository

    async def get_by_id(self, wallet_id: int) -> Wallet:
        wallet = await self._repository.get_by_id(wallet_id)

        if wallet is None:
            raise ObjectDoesNotExist()

        return wallet
