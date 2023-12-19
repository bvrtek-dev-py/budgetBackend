from typing import Dict

import pytest
from httpx import AsyncClient

from backend.main import app
from backend.modules.wallet.dependencies import get_wallet_repository
from backend.tests.conftest import login_user
from backend.tests.integration.wallet.repository import InMemoryWalletRepository

app.dependency_overrides[get_wallet_repository] = lambda: InMemoryWalletRepository()


@pytest.mark.asyncio
async def test_get_wallets(async_client: AsyncClient, test_user: Dict[str, str]):
    # Given
    token = await login_user(async_client, test_user)
    data = {"name": "Konto", "description": "description", "user_id": 1}

    # When
    response = await async_client.get(
        "/api/v1/wallets", headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json()[0].items()
    assert 1 == len(response.json())


@pytest.mark.asyncio
async def test_get_wallet_owned_wallet_by_id(
    async_client: AsyncClient, test_user: Dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    user_id = 1
    data = {"name": "Konto", "description": "description", "user_id": user_id}

    # When
    response = await async_client.get(
        f"/api/v1/wallets/{user_id}", headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()


@pytest.mark.asyncio
async def test_get_wallet_not_owned_by_id(
    async_client: AsyncClient, test_user: Dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    wallet_id = 2

    # When
    response = await async_client.get(
        f"/api/v1/wallets/{wallet_id}", headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_wallet_does_not_exist(
    async_client: AsyncClient, test_user: Dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    wallet_id = 3

    # When
    response = await async_client.get(
        f"/api/v1/wallets/{wallet_id}", headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 404
