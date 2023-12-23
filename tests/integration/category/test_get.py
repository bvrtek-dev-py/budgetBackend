import pytest
from httpx import AsyncClient

from backend.tests.conftest import login_user
from backend.tests.integration.category.data import BASE_CATEGORY_DATA, BASE_CATEGORY_ID


@pytest.mark.asyncio
async def test_get_category_by_id(async_client: AsyncClient, test_user: dict[str, str]):
    # Given
    token = await login_user(async_client, test_user)
    category_id = BASE_CATEGORY_ID

    # When
    response = await async_client.get(
        f"/api/v1/categories/{category_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 200
    assert BASE_CATEGORY_DATA.items() <= response.json().items()


@pytest.mark.asyncio
async def test_get_category_by_id_not_authenticated(async_client: AsyncClient):
    # Given
    category_id = BASE_CATEGORY_ID

    # When
    response = await async_client.get(
        f"/api/v1/categories/{category_id}",
    )

    # Then
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_category_by_id_not_owned(
    async_client: AsyncClient, test_user: dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    category_id = 2

    # When
    response = await async_client.get(
        f"/api/v1/categories/{category_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_get_category_by_id_does_not_exist(
    async_client: AsyncClient, test_user: dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    category_id = 4

    # When
    response = await async_client.get(
        f"/api/v1/categories/{category_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Then
    assert response.status_code == 404
