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
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "username1",
    }

    # When
    response = await async_client.put(
        "/api/v1/user/me",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()


@pytest.mark.asyncio
async def test_update_user_not_authenticated(async_client: AsyncClient):
    # Given
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "username1",
    }

    # When
    response = await async_client.put(
        "/api/v1/user/me",
        json=data,
    )

    # Then
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_user_duplicated_username(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "user",
    }

    # When
    response = await async_client.put(
        "/api/v1/user/me",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_update_user_owner_duplicated_username(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "username",
    }

    # When
    response = await async_client.put(
        "/api/v1/user/me",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
