from typing import Coroutine, Any

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_wallet_owned_wallet_by_id(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 1
    data = {"name": "Konto", "description": "description", "user_id": 1}

    # When
    response = await async_client.get(
        f"/api/v1/wallets/{wallet_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()


@pytest.mark.asyncio
async def test_get_wallet_not_owned_by_id(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 2

    # When
    response = await async_client.get(
        f"/api/v1/wallets/{wallet_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_wallet_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 3

    # When
    response = await async_client.get(
        f"/api/v1/wallets/{wallet_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 404
