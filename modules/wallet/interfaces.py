from abc import ABC, abstractmethod
from typing import Sequence

from backend.modules.wallet.models import Wallet


class WalletRepositoryInterface(ABC):
    @abstractmethod
    async def save(self, wallet: Wallet) -> Wallet:
        pass

    @abstractmethod
    async def update(self, wallet: Wallet) -> Wallet:
        pass

    @abstractmethod
    async def delete(self, wallet: Wallet) -> None:
        pass

    @abstractmethod
    async def get_by_user_id(self, user_id: int) -> Sequence[Wallet]:
        pass

    @abstractmethod
    async def get_by_id(self, wallet_id: int) -> Wallet | None:
        pass

    @abstractmethod
    async def get_by_user_id_and_name(self, user_id: int, name: str) -> Wallet | None:
        pass
