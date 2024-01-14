from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.setup import get_session
from backend.modules.auth.dependencies import get_current_user
from backend.modules.auth.schemas import CurrentUserData
from backend.modules.wallet.interfaces import WalletRepositoryInterface
from backend.modules.wallet.repositories import WalletRepository
from backend.modules.wallet.services import WalletService
from backend.modules.wallet.validators import WalletValidator


def get_wallet_repository(
    session: Annotated[AsyncSession, Depends(get_session)]
) -> WalletRepositoryInterface:
    return WalletRepository(session)


def get_wallet_service(
    repository: Annotated[WalletRepositoryInterface, Depends(get_wallet_repository)]
):
    return WalletService(repository)


def get_wallet_validator(
    wallet_service: Annotated[WalletService, Depends(get_wallet_service)]
) -> WalletValidator:
    return WalletValidator(wallet_service)


class WalletOwnerPermission:
    def __init__(self, parameter_name: str):
        self._parameter_name = parameter_name

    def _get_value_from_request_parameter(self, request: Request) -> int:
        return int(request.path_params.get(self._parameter_name))  # type: ignore

    async def __call__(
        self,
        request: Request,
        current_user: Annotated[CurrentUserData, Depends(get_current_user)],
        wallet_validator: Annotated[WalletValidator, Depends(get_wallet_validator)],
    ):
        await wallet_validator.user_is_wallet_owner(
            current_user.id, self._get_value_from_request_parameter(request)
        )
