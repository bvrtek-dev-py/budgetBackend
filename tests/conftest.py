import pytest
from httpx import AsyncClient

from backend.main import app


@pytest.fixture
def async_client() -> AsyncClient:
    return AsyncClient(app=app, base_url="http://test", follow_redirects=True)
