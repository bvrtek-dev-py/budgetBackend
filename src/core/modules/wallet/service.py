from typing import Optional

from backend.src.core.modules.common.exceptions import (
    ObjectAlreadyExists,
)
from backend.src.core.modules.wallet.model import Wallet
from backend.src.core.modules.wallet.repository_interface import (
    WalletRepositoryInterface,
)
from backend.src.core.modules.wallet.schemas import WalletPayloadDTO
from backend.src.core.modules.wallet.use_case import WalletRetrievalUseCase


class WalletService:
    def __init__(
        self,
        repository: WalletRepositoryInterface,
        retrieval_use_case: WalletRetrievalUseCase,
    ):
        self._repository = repository
        self._retrieval_use_case = retrieval_use_case

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
        return await self._retrieval_use_case.get_by_id(wallet_id)

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
