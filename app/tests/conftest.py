from httpx import ASGITransport, AsyncClient
import pytest

from app.core.config import settings

settings.database_url = 'sqlite+aiosqlite:///:memory:'

from app.core.db import engine
from app.main import app
from app.models import Base


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture
def async_client() -> AsyncClient:
    return AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    )
