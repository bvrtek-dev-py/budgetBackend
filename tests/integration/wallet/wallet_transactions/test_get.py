from typing import Coroutine, Any

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_transactions(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 1

    # When
    response = await async_client.get(
        f"/api/v1/wallets/{wallet_id}/transactions",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_transactions_not_authenticated(async_client: AsyncClient):
    # Given
    wallet_id = 1

    # When
    response = await async_client.get(
        f"/api/v1/wallets/{wallet_id}/transactions",
    )

    # Then
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_transactions_not_permitted(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 2

    # When
    response = await async_client.get(
        f"/api/v1/wallets/{wallet_id}/transactions",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_transactions_wallet_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 10

    # When
    response = await async_client.get(
        f"/api/v1/wallets/{wallet_id}/transactions",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 404
