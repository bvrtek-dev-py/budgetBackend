# pylint: disable=W0611,W0108,W0621
from typing import Coroutine, Any

import pytest
from httpx import AsyncClient

from backend.tests.database import BASE_USER_ID


@pytest.mark.asyncio
async def test_delete_user(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    user_id = BASE_USER_ID

    # When
    response = await async_client.delete(
        f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_user_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    user_id = 3

    # When
    response = await async_client.delete(
        f"/api/v1/users/{user_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 404
