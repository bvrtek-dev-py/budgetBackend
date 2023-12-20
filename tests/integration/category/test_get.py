import pytest
from httpx import AsyncClient

from backend.modules.transaction.enums import TransactionType
from backend.tests.conftest import login_user
from backend.tests.integration.category.data import BASE_CATEGORY_DATA, BASE_CATEGORY_ID


@pytest.mark.asyncio
async def test_get_categories(async_client: AsyncClient, test_user: dict[str, str]):
    # Given
    token = await login_user(async_client, test_user)

    # When
    response = await async_client.get(
        "/api/v1/categories/", headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_categories_expense_type(
    async_client: AsyncClient, test_user: dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    query = f"?transaction_type={TransactionType.EXPENSE.value}"

    # When
    response = await async_client.get(
        f"/api/v1/categories/{query}", headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_categories_income_type(
    async_client: AsyncClient, test_user: dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    query = f"?transaction_type={TransactionType.INCOME.value}"

    # When
    response = await async_client.get(
        f"/api/v1/categories/{query}", headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_categories_not_authenticated(async_client: AsyncClient):
    # When
    response = await async_client.get("/api/v1/categories/")

    # Then
    assert response.status_code == 401


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
