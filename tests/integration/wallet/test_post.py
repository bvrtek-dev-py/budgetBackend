from typing import Coroutine, Any

import pytest
from httpx import AsyncClient

from backend.tests.database import BASE_USER_ID


@pytest.mark.asyncio
async def test_create_wallet(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    data = {
        "name": "Wallet",
        "description": "opis",
    }

    # When
    response = await async_client.post(
        "/api/v1/wallets",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 201
    assert data.items() <= response.json().items()
    assert BASE_USER_ID == response.json()["user_id"]


@pytest.mark.asyncio
async def test_create_wallet_with_duplicated_name(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    data = {
        "name": "Konto",
        "description": "opis",
    }

    # When
    response = await async_client.post(
        "/api/v1/wallets",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 409
