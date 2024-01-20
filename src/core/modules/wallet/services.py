from typing import Optional

from backend.src.core.modules.common.exceptions import (
    ObjectDoesNotExist,
    ObjectAlreadyExists,
)
from backend.src.core.modules.wallet.interfaces import WalletRepositoryInterface
from backend.src.core.modules.wallet.models import Wallet
from backend.src.core.modules.wallet.schemas import WalletPayloadDTO


class WalletService:
    def __init__(self, repository: WalletRepositoryInterface):
        self._repository = repository

    async def create(self, user_id: int, request_dto: WalletPayloadDTO) -> Wallet:
        if await self._wallet_with_user_id_and_name_exists(user_id, request_dto.name):
            raise ObjectAlreadyExists()

        wallet = Wallet(**request_dto.model_dump(), user_id=user_id)

        return await self._repository.save(wallet)

    async def update(self, wallet_id: int, request_dto: WalletPayloadDTO) -> Wallet:
        wallet = await self.get_by_id(wallet_id)

        if await self._wallet_with_user_id_and_name_exists(
            wallet.user_id, request_dto.name, wallet.id
        ):
            raise ObjectAlreadyExists()

        for key, value in request_dto.model_dump().items():
            setattr(wallet, key, value)

        return await self._repository.update(wallet)

    async def delete(self, wallet_id: int):
        wallet = await self.get_by_id(wallet_id)

        return await self._repository.delete(wallet)

    async def get_by_id(self, wallet_id: int) -> Wallet:
        wallet = await self._repository.get_by_id(wallet_id)

        if wallet is None:
            raise ObjectDoesNotExist()

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
