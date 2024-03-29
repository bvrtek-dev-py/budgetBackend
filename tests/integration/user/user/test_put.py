# pylint: disable=W0611,W0108,W0621
from typing import Coroutine, Any

import pytest
from httpx import AsyncClient

from backend.tests.database import BASE_USER_ID


@pytest.mark.asyncio
async def test_update_user(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    user_id = BASE_USER_ID
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "username1",
    }

    # When
    response = await async_client.put(
        f"/api/v1/users/{user_id}",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()


@pytest.mark.asyncio
async def test_update_user_duplicated_username(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    user_id = BASE_USER_ID
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "user",
    }

    # When
    response = await async_client.put(
        f"/api/v1/users/{user_id}",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_update_user_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    user_id = 3
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "username1",
    }

    # When
    response = await async_client.put(
        f"/api/v1/users/{user_id}",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user_owner_duplicated_username(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    user_id = BASE_USER_ID
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "username",
    }

    # When
    response = await async_client.put(
        f"/api/v1/users/{user_id}",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
