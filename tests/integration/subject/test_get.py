from typing import Coroutine, Any

import pytest
from httpx import AsyncClient

from backend.tests.conftest import access_token
from backend.tests.database import BASE_SUBJECT_DATA, BASE_SUBJECT_ID


@pytest.mark.asyncio
async def test_get_subject_by_id(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    data = BASE_SUBJECT_DATA | {"user_id": 1}

    # When
    response = await async_client.get(
        f"/api/v1/subjects/{BASE_SUBJECT_ID}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()


@pytest.mark.asyncio
async def test_get_subject_by_id_not_authenticated(async_client: AsyncClient):
    # When
    response = await async_client.get(f"/api/v1/subjects/{BASE_SUBJECT_ID}")

    # Then
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_subject_by_id_permission_denied(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    subject_id = 2

    # When
    response = await async_client.get(
        f"/api/v1/subjects/{subject_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_subject_by_id_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    subject_id = 4

    # When
    response = await async_client.get(
        f"/api/v1/subjects/{subject_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 404
