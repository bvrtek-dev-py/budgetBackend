from typing import Coroutine, Any

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_subject(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    data = {
        "name": "name",
    }

    # When
    response = await async_client.post(
        "/api/v1/subjects/",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
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
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    data = {
        "name": "Subject 1",
    }

    # When
    response = await async_client.post(
        "/api/v1/subjects/",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_subject_duplicated_name_but_not_owned(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    data = {
        "name": "Subject 2",
    }

    # When
    response = await async_client.post(
        "/api/v1/subjects/",
        json=data,
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 201
    assert data.items() <= response.json().items()
