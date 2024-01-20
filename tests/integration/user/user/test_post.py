# pylint: disable=W0611,W0108,W0621
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient):
    # Given
    data = {
        "username": "Kamil",
        "email": "pandagmail.pl",
        "password": "string11",
        "password_confirmation": "string11",
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
        "password": "1234111111",
        "password_confirmation": "12345111111",
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
        "password": "12341111111",
        "password_confirmation": "12341111111",
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
        "password": "123411111",
        "password_confirmation": "123411111",
    }

    # When
    response = await async_client.post("/api/v1/users", json=data)

    # Then
    assert response.status_code == 409
