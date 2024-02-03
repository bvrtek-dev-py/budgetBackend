from backend.src.core.modules.common.exceptions import PermissionDenied
from backend.src.core.modules.wallet.use_case import WalletRetrievalUseCase


class WalletValidator:
    def __init__(self, retrieval_use_case: WalletRetrievalUseCase):
        self._retrieval_use_case = retrieval_use_case

    async def user_is_wallet_owner(
        self,
        user_id: int,
        wallet_id: int,
    ) -> None:
        wallet = await self._retrieval_use_case.get_by_id(wallet_id)

        if user_id != wallet.user_id:
            raise PermissionDenied()
