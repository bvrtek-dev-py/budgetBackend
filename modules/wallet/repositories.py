from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.modules.wallet.interfaces import WalletRepositoryInterface
from backend.modules.wallet.models import Wallet


class WalletRepository(WalletRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def save(self, wallet: Wallet) -> Wallet:
        self._session.add(wallet)
        await self._session.commit()

        return wallet

    async def update(self, wallet: Wallet) -> Wallet:
        await self._session.commit()
        await self._session.refresh(wallet)

        return wallet

    async def delete(self, wallet: Wallet) -> None:
        await self._session.delete(wallet)
        await self._session.commit()

    async def get_by_user_id(self, user_id: int) -> Sequence[Wallet]:
        result = await self._session.execute(
            select(Wallet)
            .where(Wallet.user_id == user_id)
            .options(selectinload(Wallet.user))
        )

        return result.scalars().all()

    async def get_by_id(self, wallet_id: int) -> Wallet | None:
        result = await self._session.execute(
            select(Wallet)
            .where(Wallet.id == wallet_id)
            .options(selectinload(Wallet.user))
        )
        return result.scalars().first()

    async def get_by_user_id_and_name(self, user_id: int, name: str) -> Wallet | None:
        result = await self._session.execute(
            select(Wallet)
            .where((Wallet.user_id == user_id) & (Wallet.name == name))
            .options(selectinload(Wallet.user))
        )

        return result.scalars().first()
