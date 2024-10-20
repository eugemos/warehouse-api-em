from http import HTTPStatus
from typing import Any

from httpx import AsyncClient
import pytest

from app.core.db import AsyncSessionLocal
from app.models import Product
from app import schemas

from ..conftest import EndpointTestCase
from .conftest import create_fixture_products_data

pytestmark = pytest.mark.anyio


@pytest.mark.usefixtures('create_products_in_db')
class TestUpdate(EndpointTestCase):
    FIXTURE_PRODUCTS_DATA = create_fixture_products_data()

    @pytest.mark.parametrize(
        'attribute',
        [
            dict(price=0),
            dict(price=100),
            dict(amount=0),
            dict(amount=100),
            dict(name='q'),
            dict(name='q'*256),
            dict(description=''),
            dict(description='qwerty'),
        ],
        ids=[
            'price=0', 'price=100', 'amount=0', 'amount=100',
            "name='q'", "name='q'*256",
            "description=''", "description='qwerty'",
        ]
    )
    async def test_put_request_with_correct_attribute_ok(
        self, async_client: AsyncClient, attribute: dict[str, Any]
    ):
        id = 2
        exp_product_updated_data = dict(
            self.FIXTURE_PRODUCTS_DATA[id-1], **attribute
        )
        exp_response_data = dict(exp_product_updated_data)
        del exp_response_data['id']
        response_data = await self._do_request_and_check_response(
            async_client, id, attribute, HTTPStatus.OK
        )
        product_updated_data = await self._get_product_data_from_db(id)
        assert response_data == exp_response_data
        assert product_updated_data == exp_product_updated_data

    @pytest.mark.parametrize(
        'attribute',
        [
            dict(price=-1),
            dict(amount=-1),
            dict(name=''),
            dict(name='q'*257),
            dict(id=100),
        ],
        ids=['price < 0', 'amount < 0', 'name empty', 'name too long', 'id']
    )
    async def test_put_request_with_incorrect_attribute_fails(
        self, async_client: AsyncClient, attribute: dict[str, Any]
    ):
        id = 2
        exp_product_updated_data = dict(self.FIXTURE_PRODUCTS_DATA[id-1])
        await self._do_request_and_check_response(
            async_client, id, attribute, HTTPStatus.UNPROCESSABLE_ENTITY
        )
        product_updated_data = await self._get_product_data_from_db(id)
        assert product_updated_data == exp_product_updated_data

    async def test_put_request_to_nonexistent_id_fails(
        self, async_client: AsyncClient
    ):
        await self._do_request_and_check_response(
            async_client,
            len(self.FIXTURE_PRODUCTS_DATA) + 1,
            dict(price=100),
            HTTPStatus.NOT_FOUND,
        )

    async def _do_request_and_check_response(
        self,
        async_client: AsyncClient,
        id: int,
        request_data: dict,
        exp_status: HTTPStatus,
    ) -> Any:
        path = f'/products/{id}'
        response = await super()._do_request_and_check_response(
            async_client, 'put', path, exp_status, json=request_data
        )
        return response.json()

    async def _get_product_data_from_db(self, id: int) -> dict[str, Any]:
        async with AsyncSessionLocal() as session:
            product = await session.get(Product, id)
            return schemas.FullProduct.model_validate(
                product, from_attributes=True
            ).model_dump(exclude_none=True)
