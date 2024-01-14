from datetime import date
from decimal import Decimal
from typing import Coroutine, Any

import pytest
from httpx import AsyncClient

from backend.modules.transaction.enums import TransactionType


@pytest.mark.asyncio
async def test_create_transaction(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 1
    data_response = {
        "name": "1name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
    }
    data_to_update = data_response | {
        "subject_id": 1,
        "category_id": 1,
        "type": TransactionType.EXPENSE,
        "value": str(Decimal(30.0)),
    }

    # When
    response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/transactions",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 201
    assert data_response.items() <= response.json().items()


@pytest.mark.asyncio
async def test_create_transaction_not_authenticated(async_client: AsyncClient):
    # Given
    wallet_id = 1
    data_response = {
        "name": "1name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {
        "subject_id": 1,
        "category_id": 1,
        "type": TransactionType.EXPENSE,
    }

    # When
    response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/transactions",
        json=data_to_update,
    )

    # Then
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_transaction_wallet_not_owned(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 2
    data_response = {
        "name": "1name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {
        "subject_id": 1,
        "category_id": 1,
        "type": TransactionType.EXPENSE,
    }

    # When
    response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/transactions",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_transaction_subject_not_owned(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 1
    data_response = {
        "name": "1name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {
        "subject_id": 2,
        "category_id": 1,
        "type": TransactionType.EXPENSE,
    }

    # When
    response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/transactions",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_transaction_category_not_owned(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 1
    data_response = {
        "name": "1name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {
        "subject_id": 1,
        "category_id": 2,
        "type": TransactionType.EXPENSE,
    }

    # When
    response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/transactions",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_create_transaction_wallet_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 10
    data_response = {
        "name": "1name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {
        "subject_id": 1,
        "category_id": 1,
        "type": TransactionType.EXPENSE,
    }

    # When
    response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/transactions",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_transaction_category_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 1
    data_response = {
        "name": "1name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {
        "subject_id": 1,
        "category_id": 10,
        "type": TransactionType.EXPENSE,
    }

    # When
    response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/transactions",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_transaction_subject_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 1
    data_response = {
        "name": "1name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {
        "subject_id": 10,
        "category_id": 1,
        "type": TransactionType.EXPENSE,
    }

    # When
    response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/transactions",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_transaction_conflict(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    wallet_id = 1
    data_response = {
        "name": "name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("20.00")),
    }
    data_to_update = data_response | {
        "subject_id": 1,
        "category_id": 1,
        "type": TransactionType.INCOME,
    }

    # When
    response = await async_client.post(
        f"/api/v1/wallets/{wallet_id}/transactions",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 409
