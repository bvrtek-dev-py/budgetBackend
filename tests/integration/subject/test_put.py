from typing import Coroutine, Any

import pytest
from httpx import AsyncClient

from backend.tests.database import BASE_SUBJECT_ID


@pytest.mark.asyncio
async def test_update_subject(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    data = {"name": "new name"}

    # When
    response = await async_client.put(
        f"/api/v1/subjects/{BASE_SUBJECT_ID}",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()


@pytest.mark.asyncio
async def test_update_subject_not_authenticated(async_client: AsyncClient):
    # Given
    data = {"name": "new name"}

    # When
    response = await async_client.put(
        f"/api/v1/subjects/{BASE_SUBJECT_ID}",
        json=data,
    )

    # Then
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_subject_permission_denied(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    data = {"name": "new name"}
    subject_id = 2

    # When
    response = await async_client.put(
        f"/api/v1/subjects/{subject_id}",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_subject_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    data = {"name": "new name"}
    subject_id = 5

    # When
    response = await async_client.put(
        f"/api/v1/subjects/{subject_id}",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_subject_conflict(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    data = {"name": "Subject 3"}

    # When
    response = await async_client.put(
        f"/api/v1/subjects/{BASE_SUBJECT_ID}",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_update_subject_same_name_but_same_object(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    data = {"name": "Subject 1"}

    # When
    response = await async_client.put(
        f"/api/v1/subjects/{BASE_SUBJECT_ID}",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()
