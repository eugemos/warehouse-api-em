from http import HTTPStatus

from httpx import ASGITransport, AsyncClient, Response
import pytest

from app.core.config import settings

settings.test_mode = True

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


class EndpointTestCase:

    async def _do_request_and_check_response(
        self,
        async_client: AsyncClient,
        method: str,
        path: str,
        exp_status: HTTPStatus,
        **kvargs,
    ) -> Response:
        async with async_client as client:
            response = await client.request(method, path, **kvargs)

        assert response.status_code == exp_status
        return response
