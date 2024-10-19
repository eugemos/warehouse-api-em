import pytest

from app.core.config import settings

settings.database_url = 'sqlite+aiosqlite:///:memory:'

from app.models import Base
from app.core.db import engine


@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture(autouse=True)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
