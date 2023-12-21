from typing import Dict

import pytest
from httpx import AsyncClient

from backend.tests.conftest import login_user
from backend.tests.integration.subject.data import BASE_SUBJECT_ID


@pytest.mark.asyncio
async def test_delete_subject(async_client: AsyncClient, test_user: Dict[str, str]):
    # Given
    token = await login_user(async_client, test_user)

    # When
    response = await async_client.delete(
        f"/api/v1/subjects/{BASE_SUBJECT_ID}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_subject_not_authenticated(async_client: AsyncClient):
    # When
    response = await async_client.delete(f"/api/v1/subjects/{BASE_SUBJECT_ID}")

    # Then
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_subject_permission_denied(
    async_client: AsyncClient, test_user: Dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    subject_id = 2

    # When
    response = await async_client.delete(
        f"/api/v1/subjects/{subject_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_subject_does_not_exist(
    async_client: AsyncClient, test_user: Dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    subject_id = 5

    # When
    response = await async_client.delete(
        f"/api/v1/subjects/{subject_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 404
