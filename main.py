import asyncio

import uvicorn
from fastapi import FastAPI
from budgetBackend.api.v1.user.routers import router as user_router
from budgetBackend.api.v1.wallet.routers import router as wallet_router
from budgetBackend.database.setup import async_engine_factory
from budgetBackend.modules.user.models import User
from budgetBackend.modules.wallet.models import Wallet

app = FastAPI()

app.include_router(user_router)
app.include_router(wallet_router)


async def create_tables():
    # Will be deleted (when add alembic)
    async with async_engine_factory().begin() as engine:
        await engine.run_sync(User.metadata.create_all)
        await engine.run_sync(Wallet.metadata.create_all)


if __name__ == "__main__":
    asyncio.run(create_tables())
    uvicorn.run(app, port=8080)
