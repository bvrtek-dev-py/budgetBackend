# pylint: disable=W0611,W0108,W0621
import pytest
from httpx import AsyncClient

from backend.tests.integration.user.data import base_user_data

from backend.tests.integration.user.repository import InMemoryUserRepository
from backend.main import app
from backend.modules.user.dependencies import get_user_repository


app.dependency_overrides[get_user_repository] = lambda: InMemoryUserRepository()


@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient):
    # Given
    data = {
        "username": "Kamil",
        "email": "pandagmail.pl",
        "password1": "string11",
        "password2": "string11",
        "first_name": "Kamil",
        "last_name": "Panda",
    }
    expected_response = {
        "username": "Kamil",
        "email": "pandagmail.pl",
        "first_name": "Kamil",
        "last_name": "Panda",
    }

    # When
    response = await async_client.post("/api/v1/users", json=data)

    # Then
    assert response.status_code == 201
    assert expected_response.items() <= response.json().items()


@pytest.mark.asyncio
async def test_create_user_password_mismatch(async_client: AsyncClient):
    # Given
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "username",
        "email": "email@email.pl",
        "password1": "1234111111",
        "password2": "12345111111",
    }

    # When
    response = await async_client.post("/api/v1/users", json=data)

    # Then
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_user_with_duplicated_email(async_client: AsyncClient):
    # Given
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "usernameaaa",
        "email": "email@email.pl",
        "password1": "12341111111",
        "password2": "12341111111",
    }

    # When
    response = await async_client.post("/api/v1/users", json=data)

    # Then
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_user_with_duplicated_username(async_client: AsyncClient):
    # Given
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "username",
        "email": "email1@email.pl",
        "password1": "123411111",
        "password2": "123411111",
    }

    # When
    response = await async_client.post("/api/v1/users", json=data)

    # Then
    assert response.status_code == 409


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
    user_id = 1
    data = base_user_data

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
async def test_update_user(async_client: AsyncClient):
    # Given
    user_id = 1
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "username1",
    }

    # When
    response = await async_client.put(f"/api/v1/users/{user_id}", json=data)

    # Then
    assert response.status_code == 200
    assert data.items() <= response.json().items()


@pytest.mark.asyncio
async def test_update_user_duplicated_username(async_client: AsyncClient):
    # Given
    user_id = 1
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "user",
    }

    # When
    response = await async_client.put(f"/api/v1/users/{user_id}", json=data)

    # Then
    assert response.status_code == 409


@pytest.mark.asyncio
async def test_update_user_does_not_exist(async_client: AsyncClient):
    # Given
    user_id = 3
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "username1",
    }

    # When
    response = await async_client.put(f"/api/v1/users/{user_id}", json=data)

    # Then
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_user_owner_duplicated_username(async_client: AsyncClient):
    # Given
    user_id = 1
    data = {
        "first_name": "name",
        "last_name": "last",
        "username": "username",
    }

    # When
    response = await async_client.put(f"/api/v1/users/{user_id}", json=data)

    # Then
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_user(async_client: AsyncClient):
    # Given
    user_id = 1

    # When
    response = await async_client.delete(f"/api/v1/users/{user_id}")

    # Then
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_user_does_not_exist(async_client: AsyncClient):
    # Given
    user_id = 3

    # When
    response = await async_client.delete(f"/api/v1/users/{user_id}")

    # Then
    assert response.status_code == 404
