from http import HTTPStatus
from typing import Any

from httpx import AsyncClient
import pytest

from app.core.db import AsyncSessionLocal
from app.core.types import OrderStatus
from app.models import Product
from app.repos import OrderRepo

from ..conftest import EndpointTestCase
from .conftest import FIXTURE_PRODUCTS_COUNT

pytestmark = pytest.mark.anyio


@pytest.fixture
async def fill_db(create_products_in_db):
    async with AsyncSessionLocal() as session:
        order_repo = OrderRepo(session)
        await order_repo.create(
            OrderStatus.PROCESSING,
            [dict(product_id=1, amount=1)]
        )


@pytest.mark.usefixtures('fill_db')
class TestDelete(EndpointTestCase):
    async def test_delete_request_for_unordered_product_ok(
        self, async_client: AsyncClient
    ):
        id = FIXTURE_PRODUCTS_COUNT
        await self._do_request_and_check_response(
            async_client, id, HTTPStatus.NO_CONTENT
        )
        assert await self._product_deleted(id)

    async def test_delete_request_for_ordered_product_fails(
        self, async_client: AsyncClient
    ):
        id = 1
        await self._do_request_and_check_response(
            async_client, id, HTTPStatus.UNPROCESSABLE_ENTITY
        )
        assert not await self._product_deleted(id)

    async def test_delete_request_to_nonexistent_id_fails(
        self, async_client: AsyncClient
    ):
        id = FIXTURE_PRODUCTS_COUNT + 1
        await self._do_request_and_check_response(
            async_client, id, HTTPStatus.NOT_FOUND
        )

    async def _product_deleted(self, id) -> bool:
        async with AsyncSessionLocal() as session:
            product = await session.get(Product, id)
            return product is None

    async def _do_request_and_check_response(
        self,
        async_client: AsyncClient,
        id: int,
        exp_status: HTTPStatus,
    ) -> Any:
        await super()._do_request_and_check_response(
            async_client, 'delete', f'/products/{id}', exp_status
        )
