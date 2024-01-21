from backend.src.core.modules.common.exceptions import PermissionDenied
from backend.src.core.modules.wallet.service import WalletService


class WalletValidator:
    def __init__(self, wallet_service: WalletService):
        self._wallet_service = wallet_service

    async def user_is_wallet_owner(
        self,
        user_id: int,
        wallet_id: int,
    ) -> None:
        wallet = await self._wallet_service.get_by_id(wallet_id)

        if user_id != wallet.user_id:
            raise PermissionDenied()
