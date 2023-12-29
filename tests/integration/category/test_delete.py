import pytest
from httpx import AsyncClient

from backend.tests.conftest import login_user
from backend.tests.database import BASE_CATEGORY_ID


@pytest.mark.asyncio
async def test_delete_category(async_client: AsyncClient, test_user: dict[str, str]):
    # Given
    token = await login_user(async_client, test_user)
    category_id = BASE_CATEGORY_ID

    # When
    response = await async_client.delete(
        f"/api/v1/categories/{category_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_category_not_authenticated(async_client: AsyncClient):
    # Given
    category_id = BASE_CATEGORY_ID

    # When
    response = await async_client.delete(f"/api/v1/categories/{category_id}")

    # Then
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_delete_category_not_owned(
    async_client: AsyncClient, test_user: dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    category_id = 2

    # When
    response = await async_client.delete(
        f"/api/v1/categories/{category_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_delete_category_does_not_exist(
    async_client: AsyncClient, test_user: dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    category_id = 5

    # When
    response = await async_client.delete(
        f"/api/v1/categories/{category_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 404
