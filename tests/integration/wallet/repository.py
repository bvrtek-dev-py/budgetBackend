from typing import List, Optional

from backend.modules.wallet.interfaces import WalletRepositoryInterface
from backend.modules.wallet.models import Wallet
from backend.tests.integration.wallet.data import get_wallet_data


class InMemoryWalletRepository(WalletRepositoryInterface):
    def __init__(self):
        self._wallets: List[Wallet] = get_wallet_data()

    async def save(self, wallet: Wallet) -> Wallet:
        # Simulate auto-incrementing ID
        wallet_id = len(self._wallets) + 1
        wallet.id = wallet_id

        self._wallets.append(wallet)
        return wallet

    async def update(self, wallet: Wallet) -> Wallet:
        return wallet

    async def delete(self, wallet: Wallet) -> None:
        self._wallets.remove(wallet)

    async def get_by_user_id(self, user_id: int) -> List[Wallet]:
        return [wallet for wallet in self._wallets if wallet.user_id == user_id]

    async def get_by_id(self, wallet_id: int) -> Optional[Wallet]:
        for wallet in self._wallets:
            if wallet.id == wallet_id:
                return wallet

        return None

    async def get_by_user_id_and_name(
        self, user_id: int, name: str
    ) -> Optional[Wallet]:
        for wallet in self._wallets:
            if wallet.user_id == user_id and wallet.name == name:
                return wallet

        return None
