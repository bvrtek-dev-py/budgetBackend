from typing import Coroutine, Any

import pytest
from httpx import AsyncClient

from backend.tests.database import BASE_TRANSACTION_RESPONSE


@pytest.mark.asyncio
async def test_get_transaction(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    transaction_id = 1

    # When
    response = await async_client.get(
        f"/api/v1/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert BASE_TRANSACTION_RESPONSE.items() <= response.json().items()


@pytest.mark.asyncio
async def test_get_transaction_not_authenticated(async_client: AsyncClient):
    # Given
    transaction_id = 1

    # When
    response = await async_client.get(
        f"/api/v1/transactions/{transaction_id}",
    )

    # Then
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_transaction_not_permitted(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    transaction_id = 3

    # When
    response = await async_client.get(
        f"/api/v1/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_transaction_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    transaction_id = 10

    # When
    response = await async_client.get(
        f"/api/v1/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 404
