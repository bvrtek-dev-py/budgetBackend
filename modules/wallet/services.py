from typing import Sequence

from backend.modules.common.exceptions import ObjectDoesNotExist
from backend.modules.wallet.models import Wallet
from backend.modules.wallet.repositories import WalletRepository


class WalletService:
    def __init__(self, repository: WalletRepository):
        self._repository = repository

    async def create(self, name: str, description: str) -> Wallet:
        wallet = Wallet(name=name, description=description)

        return await self._repository.save(wallet)

    async def update(self, wallet_id: int, name: str, description: str) -> Wallet:
        wallet = await self.get_by_id(wallet_id)

        wallet.name = name
        wallet.description = description

        return await self._repository.update(wallet)

    async def delete(self, wallet_id: int):
        wallet = await self.get_by_id(wallet_id)

        return await self._repository.delete(wallet)

    async def get_by_id(self, wallet_id: int) -> Wallet:
        wallet = await self._repository.get_by_id(wallet_id)

        if wallet is None:
            raise ObjectDoesNotExist

        return wallet

    async def get_all(self) -> Sequence[Wallet]:
        return await self._repository.get_all()
