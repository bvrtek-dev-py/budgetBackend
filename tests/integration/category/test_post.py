import pytest
from httpx import AsyncClient

from backend.tests.conftest import login_user
from backend.tests.integration.category.data import BASE_CATEGORY_DATA
from backend.tests.integration.user.data import BASE_USER_ID


@pytest.mark.asyncio
async def test_create_category(async_client: AsyncClient, test_user: dict[str, str]):
    # Given
    token = await login_user(async_client, test_user)
    data = {
        "name": "new category",
        "transaction_type": "income",
    }

    # When
    response = await async_client.post(
        "/api/v1/categories/", json=data, headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 201
    assert data.items() <= response.json().items()
    assert BASE_USER_ID == response.json()["user_id"]


@pytest.mark.asyncio
async def test_create_category_name_exists_same_user(
    async_client: AsyncClient, test_user: dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    data = {
        "name": BASE_CATEGORY_DATA["name"],
        "transaction_type": "income",
    }

    # When
    response = await async_client.post(
        "/api/v1/categories/", json=data, headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_category_name_exists_for_different_user(
    async_client: AsyncClient, test_user: dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    data = {
        "name": "Category 2",
        "transaction_type": "income",
    }

    # When
    response = await async_client.post(
        "/api/v1/categories/", json=data, headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 201
    assert data.items() <= response.json().items()
    assert BASE_USER_ID == response.json()["user_id"]


@pytest.mark.asyncio
async def test_create_category_not_authenticated(async_client: AsyncClient):
    # Given
    data = {
        "name": "new category",
        "transaction_type": "income",
    }

    # When
    response = await async_client.post("/api/v1/categories/", json=data)

    # Then
    assert response.status_code == 401
