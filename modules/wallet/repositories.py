from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.modules.wallet.models import Wallet


class WalletRepository:
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

    async def get_all(self) -> Sequence[Wallet]:
        result = await self._session.execute(select(Wallet))

        return result.scalars().all()

    async def get_by_id(self, wallet_id: int) -> Wallet | None:
        return await self._session.get(Wallet, wallet_id)
