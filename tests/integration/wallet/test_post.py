import pytest
from httpx import AsyncClient

from backend.main import app
from backend.modules.wallet.dependencies import get_wallet_repository
from backend.tests.conftest import login_user
from backend.tests.integration.wallet.repository import InMemoryWalletRepository

app.dependency_overrides[get_wallet_repository] = lambda: InMemoryWalletRepository()


@pytest.mark.asyncio
async def test_create_wallet(async_client: AsyncClient, test_user: dict[str, str]):
    # Given
    token = await login_user(async_client, test_user)
    data = {
        "name": "Wallet",
        "description": "opis",
    }

    # When
    response = await async_client.post(
        "/api/v1/wallets", json=data, headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 201
    assert data.items() <= response.json().items()
    assert 1 == response.json()["user_id"]


@pytest.mark.asyncio
async def test_create_wallet_with_duplicated_name(
    async_client: AsyncClient, test_user: dict[str, str]
):
    # Given
    token = await login_user(async_client, test_user)
    data = {
        "name": "Konto",
        "description": "opis",
    }

    # When
    response = await async_client.post(
        "/api/v1/wallets", json=data, headers={"Authorization": f"Bearer {token}"}
    )

    # Then
    assert response.status_code == 409
