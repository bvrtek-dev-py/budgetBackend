from typing import Coroutine, Any

import pytest
from httpx import AsyncClient

from backend.tests.conftest import access_token
from backend.tests.database import BASE_WALLET_ID


@pytest.mark.asyncio
async def test_delete_wallet(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = BASE_WALLET_ID

    # When
    response = await async_client.delete(
        f"/api/v1/wallets/{wallet_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_wallet_not_owned(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 2

    # When
    response = await async_client.delete(
        f"/api/v1/wallets/{wallet_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_wallet_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 3

    # When
    response = await async_client.delete(
        f"/api/v1/wallets/{wallet_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 404
