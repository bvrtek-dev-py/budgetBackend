# pylint: disable=W0621,W0108
from typing import Dict

import pytest
from httpx import AsyncClient

from backend.main import app
from backend.modules.wallet.dependencies import get_wallet_repository
from backend.tests.integration.user.data import get_user_db
from backend.tests.integration.wallet.repository import InMemoryWalletRepository

app.dependency_overrides[get_wallet_repository] = lambda: InMemoryWalletRepository()


@pytest.fixture
def async_client() -> AsyncClient:
    return AsyncClient(app=app, base_url="http://test", follow_redirects=True)


@pytest.fixture
def test_user() -> Dict[str, str]:
    users = get_user_db()
    return {"username": users[0].username, "password": "1234"}


async def login_user(async_client: AsyncClient, test_user: Dict[str, str]):
    response = await async_client.post("/api/v1/auth/login", data=test_user)
    return response.json()["access_token"]
