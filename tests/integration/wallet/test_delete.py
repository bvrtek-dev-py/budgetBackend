from typing import Dict

import pytest
from httpx import AsyncClient

from backend.tests.conftest import login_user


@pytest.mark.asyncio
async def test_delete_wallet(async_client: AsyncClient, test_user: Dict[str, str]):
    # Given
    token = await login_user(async_client, test_user)
    wallet_id = 1

    # When
    response = await async_client.delete(
        f"/api/v1/wallets/{wallet_id}", headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_wallet_not_owned(
    async_client: AsyncClient, test_user: Dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    wallet_id = 2

    # When
    response = await async_client.delete(
        f"/api/v1/wallets/{wallet_id}", headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_wallet_does_not_exist(
    async_client: AsyncClient, test_user: Dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    wallet_id = 3

    # When
    response = await async_client.delete(
        f"/api/v1/wallets/{wallet_id}", headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 404
