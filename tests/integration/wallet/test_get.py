from typing import Dict

import pytest
from httpx import AsyncClient

from backend.tests.conftest import login_user
from backend.tests.database import BASE_USER_ID


@pytest.mark.asyncio
async def test_get_wallet_owned_wallet_by_id(
    async_client: AsyncClient, test_user: Dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    user_id = BASE_USER_ID
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
