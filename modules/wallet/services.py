from typing import Sequence, Optional

from backend.modules.common.exceptions import ObjectDoesNotExist, ObjectAlreadyExists
from backend.modules.wallet.interfaces import WalletRepositoryInterface
from backend.modules.wallet.models import Wallet


class WalletService:
    def __init__(self, repository: WalletRepositoryInterface):
        self._repository = repository

    async def create(self, user_id: int, name: str, description: str) -> Wallet:
        if await self._wallet_with_user_id_and_name_exists(user_id, name):
            raise ObjectAlreadyExists

        wallet = Wallet(name=name, description=description, user_id=user_id)

        return await self._repository.save(wallet)

    async def update(self, wallet_id: int, name: str, description: str) -> Wallet:
        wallet = await self.get_by_id(wallet_id)

        if await self._wallet_with_user_id_and_name_exists(
            wallet.user_id, name, wallet.id
        ):
            raise ObjectAlreadyExists

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

    async def _wallet_with_user_id_and_name_exists(
        self, user_id: int, name: str, exclude_wallet_id: Optional[int] = None
    ) -> bool:
        """
        Method checks if object with user_id and name already exists and if this object
        is not excluded.
        """
        wallet = await self._repository.get_by_user_id_and_name(user_id, name)

        if wallet is None or wallet.id == exclude_wallet_id:
            return False

        return True

    async def get_by_user_id(self, user_id: int) -> Sequence[Wallet]:
        return await self._repository.get_by_user_id(user_id)
