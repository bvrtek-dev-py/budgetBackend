from datetime import date
from decimal import Decimal
from typing import Coroutine, Any

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_update_transaction(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    transaction_id = 1
    data_response = {
        "name": "name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {"subject_id": 1, "category_id": 1}

    # When
    response = await async_client.put(
        f"/api/v1/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 200
    assert data_response.items() <= response.json().items()


@pytest.mark.asyncio
async def test_update_transaction_not_authenticated(async_client: AsyncClient):
    # Given
    transaction_id = 1
    data_response = {
        "name": "name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {"subject_id": 1, "category_id": 1}

    # When
    response = await async_client.put(
        f"/api/v1/transactions/{transaction_id}",
        json=data_to_update,
    )

    # Then
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_update_transaction_not_permitted(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    transaction_id = 3
    data_response = {
        "name": "name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {"subject_id": 1, "category_id": 1}

    # When
    response = await async_client.put(
        f"/api/v1/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_transaction_not_owned_subject(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    transaction_id = 1
    data_response = {
        "name": "1name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {"subject_id": 2, "category_id": 1}

    # When
    response = await async_client.put(
        f"/api/v1/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_transaction_not_owned_category(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    transaction_id = 1
    data_response = {
        "name": "11name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {"subject_id": 1, "category_id": 2}

    # When
    response = await async_client.put(
        f"/api/v1/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 403


@pytest.mark.asyncio
async def test_update_transaction_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    transaction_id = 10
    data_response = {
        "name": "name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {"subject_id": 1, "category_id": 1}

    # When
    response = await async_client.put(
        f"/api/v1/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_transaction_subject_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    transaction_id = 1
    data_response = {
        "name": "n11ame",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {"subject_id": 40, "category_id": 1}

    # When
    response = await async_client.put(
        f"/api/v1/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_transaction_category_does_not_exist(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    transaction_id = 1
    data_response = {
        "name": "name11",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("30.00")),
    }
    data_to_update = data_response | {"subject_id": 1, "category_id": 15}

    # When
    response = await async_client.put(
        f"/api/v1/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_transaction_conflict(
    async_client: AsyncClient, access_token: Coroutine[Any, Any, str]
):
    # Given
    transaction_id = 2
    data_response = {
        "name": "name",
        "description": "description",
        "date": date.today().strftime("%Y-%m-%d"),
        "value": str(Decimal("20.00")),
    }
    data_to_update = data_response | {"subject_id": 1, "category_id": 1}

    # When
    response = await async_client.put(
        f"/api/v1/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {await access_token}"},
        json=data_to_update,
    )

    # Then
    assert response.status_code == 409
