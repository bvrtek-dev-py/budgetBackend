from typing import Dict

import pytest
from httpx import AsyncClient

from backend.tests.conftest import login_user


@pytest.mark.asyncio
async def test_create_subject(async_client: AsyncClient, test_user: Dict[str, str]):
    # Given
    access_token = await login_user(async_client, test_user)
    data = {
        "name": "name",
    }

    # When
    response = await async_client.post(
        "/api/v1/subjects/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Then
    assert response.status_code == 201
    assert data.items() <= response.json().items()


@pytest.mark.asyncio
async def test_create_subject_not_authenticated(async_client: AsyncClient):
    # Given
    data = {
        "name": "name",
    }

    # When
    response = await async_client.post("/api/v1/subjects/", json=data)

    # Then
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_subject_conflict(
    async_client: AsyncClient, test_user: Dict[str, str]
):
    # Given
    access_token = await login_user(async_client, test_user)
    data = {
        "name": "Subject 1",
    }

    # When
    response = await async_client.post(
        "/api/v1/subjects/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Then
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_subject_duplicated_name_but_not_owned(
    async_client: AsyncClient, test_user: Dict[str, str]
):
    # Given
    access_token = await login_user(async_client, test_user)
    data = {
        "name": "Subject 2",
    }

    # When
    response = await async_client.post(
        "/api/v1/subjects/",
        json=data,
        headers={"Authorization": f"Bearer {access_token}"},
    )

    # Then
    assert response.status_code == 201
    assert data.items() <= response.json().items()
