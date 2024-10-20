from http import HTTPStatus
from typing import Any

from httpx import AsyncClient
import pytest

from ..conftest import EndpointTestCase
from .conftest import create_fixture_products_data

pytestmark = pytest.mark.anyio


@pytest.mark.usefixtures('create_products_in_db')
class TestGet(EndpointTestCase):
    FIXTURE_PRODUCTS_DATA = create_fixture_products_data()

    @pytest.mark.parametrize(
        'id', list(range(1, len(FIXTURE_PRODUCTS_DATA)+1))
    )
    async def test_get_request_to_existing_id_ok(
        self, async_client: AsyncClient, id: int
    ):
        exp_response_data = dict(self.FIXTURE_PRODUCTS_DATA[id-1])
        del exp_response_data['id']
        response_data = await self._do_request_and_check_response(
            async_client, id, HTTPStatus.OK
        )
        assert response_data == exp_response_data

    async def test_get_request_to_nonexistent_id_fails(
        self, async_client: AsyncClient
    ):
        await self._do_request_and_check_response(
            async_client,
            len(self.FIXTURE_PRODUCTS_DATA) + 1,
            HTTPStatus.NOT_FOUND,
        )

    async def _do_request_and_check_response(
        self,
        async_client: AsyncClient,
        id: int,
        exp_status: HTTPStatus,
    ) -> Any:
        response = await super()._do_request_and_check_response(
            async_client, 'get', f'/products/{id}', exp_status
        )
        return response.json()
