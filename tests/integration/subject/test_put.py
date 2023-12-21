from typing import Dict

import pytest
from httpx import AsyncClient

from backend.tests.conftest import login_user
from backend.tests.integration.subject.data import BASE_SUBJECT_ID


@pytest.mark.asyncio
async def test_update_subject(async_client: AsyncClient, test_user: Dict[str, str]):
    # Given
    token = await login_user(async_client, test_user)
    data = {"name": "new name"}

    # When
    response = await async_client.put(
        f"/api/v1/subjects/{BASE_SUBJECT_ID}",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
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
    async_client: AsyncClient, test_user: Dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    data = {"name": "new name"}
    subject_id = 2

    # When
    response = await async_client.put(
        f"/api/v1/subjects/{subject_id}",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_subject_does_not_exist(
    async_client: AsyncClient, test_user: Dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    data = {"name": "new name"}
    subject_id = 5

    # When
    response = await async_client.put(
        f"/api/v1/subjects/{subject_id}",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_subject_conflict(
    async_client: AsyncClient, test_user: Dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    data = {"name": "Subject 3"}

    # When
    response = await async_client.put(
        f"/api/v1/subjects/{BASE_SUBJECT_ID}",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_update_subject_same_name_but_same_object(
    async_client: AsyncClient, test_user: Dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    data = {"name": "Subject 1"}

    # When
    response = await async_client.put(
        f"/api/v1/subjects/{BASE_SUBJECT_ID}",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()
