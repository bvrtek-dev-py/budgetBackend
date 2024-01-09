# pylint: disable=W0611,W0108,W0621
from typing import Coroutine, Any

import pytest
from httpx import AsyncClient

from backend.modules.transaction.enums import TransactionType
from backend.tests.database import BASE_USER_ID, BASE_USER_DATA, BASE_WALLET_DATA


@pytest.mark.asyncio
async def test_get_users(async_client: AsyncClient):
    # When
    response = await async_client.get("/api/v1/users")

    # Then
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_user_by_id(async_client: AsyncClient):
    # Given
    user_id = BASE_USER_ID
    data = BASE_USER_DATA

    # When
    response = await async_client.get(f"/api/v1/users/{user_id}")

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()


@pytest.mark.asyncio
async def test_get_user_by_id_does_not_exist(async_client: AsyncClient):
    # Given
    user_id = 3

    # When
    response = await async_client.get(f"/api/v1/users/{user_id}")

    # Then
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_categories(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # When
    response = await async_client.get(
        "/api/v1/users/me/categories/",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_get_categories_expense_type(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    query = f"?transaction_type={TransactionType.EXPENSE.value}"

    # When
    response = await async_client.get(
        f"/api/v1/users/me/categories/{query}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_categories_income_type(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    query = f"?transaction_type={TransactionType.INCOME.value}"

    # When
    response = await async_client.get(
        f"/api/v1/users/me/categories/{query}",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest.mark.asyncio
async def test_get_categories_not_authenticated(async_client: AsyncClient):
    # When
    response = await async_client.get("/api/v1/users/me/categories/")

    # Then
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_wallets(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    data = BASE_WALLET_DATA

    # When
    response = await async_client.get(
        "/api/v1/users/me/wallets",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json()[0].items()
    assert 1 == len(response.json())


@pytest.mark.asyncio
async def test_get_subjects(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # When
    response = await async_client.get(
        "/api/v1/users/me/subjects/",
        headers={"Authorization": f"Bearer {await access_token}"},
    )

    # Then
    assert response.status_code == 200
    assert len(response.json()) == 1
