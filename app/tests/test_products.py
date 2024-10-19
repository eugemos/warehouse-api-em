from http import HTTPStatus
from typing import Any

from httpx import ASGITransport, AsyncClient
import pytest
from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.main import app
from app.models import Product
from app import schemas

pytestmark = pytest.mark.anyio


@pytest.fixture
def async_client() -> AsyncClient:
    return AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    )


class TestCreate:
    REQUEST_DATA = dict(
        name='Product',
        description='Description',
        price=1,
        amount=10,
    )

    async def test_correct_full_request_creates_product(
        self, async_client: AsyncClient
    ):
        request_data = self.REQUEST_DATA
        response_data = await self._do_request_and_check_response(
            async_client, request_data, HTTPStatus.CREATED
        )
        product_created_data = await self._check_product_created_in_db()
        exp_response_data = dict(request_data, id=product_created_data['id'])
        assert product_created_data == exp_response_data
        assert response_data == exp_response_data

    async def test_correct_request_without_description_creates_product(
        self, async_client: AsyncClient
    ):
        request_data = dict(self.REQUEST_DATA)
        del request_data['description']
        response_data = await self._do_request_and_check_response(
            async_client, request_data, HTTPStatus.CREATED
        )
        product_created_data = await self._check_product_created_in_db()
        exp_product_created_data = dict(
            request_data, description=None, id=product_created_data['id']
        )
        exp_response_data = dict(request_data, id=product_created_data['id'])
        assert product_created_data == exp_product_created_data
        assert response_data == exp_response_data

    @pytest.mark.parametrize(
        'invalid_attribute',
        [
            dict(name='price', value=-1),
            dict(name='amount', value=-1),
            dict(name='name', value=''),
            dict(name='name', value='a'*257),
        ],
        ids=['price < 0', 'amount < 0', 'empty name', 'name length > 256']
    )
    async def test_request_with_invalid_attribute_fails(
        self, invalid_attribute: dict[str, Any], async_client: AsyncClient
    ):
        request_data = dict(self.REQUEST_DATA)
        request_data[invalid_attribute['name']] = invalid_attribute['value']
        await self._do_request_and_check_response(
            async_client, request_data, HTTPStatus.UNPROCESSABLE_ENTITY
        )
        await self._check_product_not_created_in_db()

    @pytest.mark.parametrize(
        'omitted_attribute',
        ['price', 'amount', 'name',],
    )
    async def test_request_with_omitted_required_attribute_fails(
        self, omitted_attribute: str, async_client: AsyncClient
    ):
        request_data = dict(self.REQUEST_DATA)
        del request_data[omitted_attribute]
        await self._do_request_and_check_response(
            async_client, request_data, HTTPStatus.UNPROCESSABLE_ENTITY
        )
        await self._check_product_not_created_in_db()

    async def _do_request_and_check_response(
        self,
        async_client: AsyncClient,
        request_data: dict,
        exp_status: HTTPStatus,
    ):
        async with async_client as client:
            response = await client.post("/products", json=request_data)

        assert response.status_code == exp_status
        return response.json()

    async def _check_product_created_in_db(self) -> dict:
        async with AsyncSessionLocal() as session:
            sqla_result = await session.scalars(select(Product))
            products_in_db = sqla_result.all()
            assert len(products_in_db) == 1
            product_created = products_in_db[0]
            return schemas.CreateProductResponse.model_validate(
                product_created, from_attributes=True
            ).model_dump()

    async def _check_product_not_created_in_db(self) -> None:
        async with AsyncSessionLocal() as session:
            sqla_result = await session.scalars(select(Product))
            products_in_db = sqla_result.all()
            assert len(products_in_db) == 0
