from abc import ABC
from typing import Sequence

from backend.modules.wallet.models import Wallet


class WalletRepositoryInterface(ABC):
    async def save(self, wallet: Wallet) -> Wallet:
        pass

    async def update(self, wallet: Wallet) -> Wallet:
        pass

    async def delete(self, wallet: Wallet) -> None:
        pass

    async def get_by_user_id(self, user_id: int) -> Sequence[Wallet]:
        pass

    async def get_by_id(self, wallet_id: int) -> Wallet | None:
        pass

    async def get_by_user_id_and_name(self, user_id: int, name: str) -> Wallet | None:
        pass
