from typing import Coroutine, Any

import pytest
from httpx import AsyncClient

from backend.tests.conftest import access_token
from backend.tests.database import BASE_WALLET_ID


@pytest.mark.asyncio
async def test_update_wallet(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = BASE_WALLET_ID
    data = {
        "name": "Konto_11",
        "description": "opisss",
    }

    # When
    response = await async_client.put(
        f"/api/v1/wallets/{wallet_id}",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()


@pytest.mark.asyncio
async def test_update_wallet_name_exists_same_wallet_id(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = BASE_WALLET_ID
    data = {
        "name": "Konto",
        "description": "opisss",
    }

    # When
    response = await async_client.put(
        f"/api/v1/wallets/{wallet_id}",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()


@pytest.mark.asyncio
async def test_update_not_owned_wallet(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 2
    data = {
        "name": "Konto",
        "description": "opisss",
    }

    # When
    response = await async_client.put(
        f"/api/v1/wallets/{wallet_id}",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_wallet_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 3
    data = {
        "name": "Konto",
        "description": "opisss",
    }

    # When
    response = await async_client.put(
        f"/api/v1/wallets/{wallet_id}",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 404
