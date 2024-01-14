# pylint: disable=W0611,W0108,W0621

import pytest
from httpx import AsyncClient

from backend.tests.database import BASE_USER_ID, BASE_USER_DATA


@pytest.mark.asyncio
async def test_get_users(async_client: AsyncClient):
    # When
    response = await async_client.get("/api/v1/users")

    # Then
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_user_by_id(async_client: AsyncClient):
    # Given
    user_id = BASE_USER_ID
    data = BASE_USER_DATA

    # When
    response = await async_client.get(f"/api/v1/users/{user_id}")

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()


@pytest.mark.asyncio
async def test_get_user_by_id_does_not_exist(async_client: AsyncClient):
    # Given
    user_id = 3

    # When
    response = await async_client.get(f"/api/v1/users/{user_id}")

    # Then
    assert response.status_code == 404
