from http import HTTPStatus
from typing import Any

from httpx import AsyncClient
import pytest

from ..conftest import EndpointTestCase
from .conftest import create_fixture_products_data

pytestmark = pytest.mark.anyio


@pytest.mark.usefixtures('create_products_in_db')
class TestList(EndpointTestCase):

    async def test_list_request_ok(self, async_client: AsyncClient):
        exp_response_data = create_fixture_products_data()
        response_data = await self._do_request_and_check_response(
            async_client, HTTPStatus.OK
        )
        assert response_data == exp_response_data

    async def _do_request_and_check_response(
        self,
        async_client: AsyncClient,
        exp_status: HTTPStatus,
    ) -> Any:
        response = await super()._do_request_and_check_response(
            async_client, 'get', '/products', exp_status
        )
        return response.json()
