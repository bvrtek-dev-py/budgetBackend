# pylint: disable=W0611,W0108,W0621
import pytest
from httpx import AsyncClient

from backend.api.v1.user.tests.data import base_user_data

from backend.api.v1.user.tests.test_repository import InMemoryUserRepository
from backend.main import app
from backend.modules.user.dependencies import get_user_repository


app.dependency_overrides[get_user_repository] = lambda: InMemoryUserRepository()


@pytest.fixture
def async_client() -> AsyncClient:
    return AsyncClient(app=app, base_url="http://test", follow_redirects=True)


@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient):
    # Given
    data = {
        "username": "Kamil",
        "email": "pandagmail.pl",
        "password1": "string",
        "password2": "string",
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
        "password1": "1234",
        "password2": "12345",
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
        "password1": "1234",
        "password2": "1234",
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
        "password1": "1234",
        "password2": "1234",
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
    assert len(response.json()) == 1


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
async def test_update_user_duplicated_username(async_client: AsyncClient):
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
    assert response.status_code == 409


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
