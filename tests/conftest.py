# pylint: disable=W0621,W0108
from typing import Dict, Any

import pytest
from httpx import AsyncClient

from backend.src.dependencies.category.creators import get_category_repository
from backend.src.dependencies.subject.creators import get_subject_repository
from backend.src.dependencies.transaction.creators import get_transaction_repository
from backend.src.dependencies.user.creators import get_user_repository
from backend.src.dependencies.wallet.creators import get_wallet_repository
from backend.src.main import app
from backend.tests.database import get_user_db
from backend.tests.integration.category.repository import InMemoryCategoryRepository
from backend.tests.integration.subject.repository import InMemorySubjectRepository
from backend.tests.integration.transaction.repository import (
    InMemoryTransactionRepository,
)
from backend.tests.integration.user.repository import InMemoryUserRepository
from backend.tests.integration.wallet.repository import InMemoryWalletRepository

app.dependency_overrides[get_user_repository] = lambda: InMemoryUserRepository()
app.dependency_overrides[get_wallet_repository] = lambda: InMemoryWalletRepository()
app.dependency_overrides[get_category_repository] = lambda: InMemoryCategoryRepository()
app.dependency_overrides[get_subject_repository] = lambda: InMemorySubjectRepository()
app.dependency_overrides[
    get_transaction_repository
] = lambda: InMemoryTransactionRepository()


@pytest.fixture
def async_client() -> AsyncClient:
    return AsyncClient(app=app, base_url="http://test", follow_redirects=True)


@pytest.fixture
def test_user() -> Dict[str, str]:
    users = get_user_db()
    return {"username": users[0].username, "password": "1234"}


@pytest.fixture
async def access_token(async_client: AsyncClient, test_user: Dict[str, str]) -> Any:
    response = await async_client.post("/api/v1/auth/login", data=test_user)
    return response.json()["access_token"]
