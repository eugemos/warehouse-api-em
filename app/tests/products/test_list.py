from http import HTTPStatus
from typing import Any

from httpx import AsyncClient
import pytest
from sqlalchemy import insert

from app.core.db import AsyncSessionLocal
from app.models import Product

from ..base import EndpointTestCase

pytestmark = pytest.mark.anyio


def create_product_data(n: int | str, **kvargs):
    return dict(
        name=f'Product{n}',
        description=f'Description{n}',
        price=1,
        amount=10,
        **kvargs
    )


def create_fixture_products_data():
    data = [
        create_product_data(i, id=i) for i in range(1, 4)
    ]
    del data[1]['description']
    return data


@pytest.fixture
async def create_products_in_db():
    products_data = create_fixture_products_data()
    async with AsyncSessionLocal() as session:
        await session.execute(insert(Product), products_data)
        await session.commit()


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
