import pytest
from httpx import AsyncClient

from backend.tests.conftest import login_user
from backend.tests.database import BASE_CATEGORY_ID


@pytest.mark.asyncio
async def test_update_category(async_client: AsyncClient, test_user: dict[str, str]):
    # Given
    token = await login_user(async_client, test_user)
    category_id = BASE_CATEGORY_ID
    data = {
        "name": "new category",
    }

    # When
    response = await async_client.put(
        f"/api/v1/categories/{category_id}",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()


@pytest.mark.asyncio
async def test_update_category_owned_name_exists(
    async_client: AsyncClient, test_user: dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    category_id = BASE_CATEGORY_ID
    data = {
        "name": "Category 3",
    }

    # When
    response = await async_client.put(
        f"/api/v1/categories/{category_id}",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_update_category_not_owned_name_exists(
    async_client: AsyncClient, test_user: dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    category_id = BASE_CATEGORY_ID
    data = {
        "name": "Category 2",
    }

    # When
    response = await async_client.put(
        f"/api/v1/categories/{category_id}",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()


@pytest.mark.asyncio
async def test_update_category_not_authenticated(async_client: AsyncClient):
    # Given
    category_id = BASE_CATEGORY_ID
    data = {
        "name": "Category 2",
    }

    # When
    response = await async_client.put(
        f"/api/v1/categories/{category_id}",
        json=data,
    )

    # Then
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_category_not_owned(
    async_client: AsyncClient, test_user: dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    category_id = 2
    data = {
        "name": "Category 22",
    }

    # When
    response = await async_client.put(
        f"/api/v1/categories/{category_id}",
        json=data,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 403
