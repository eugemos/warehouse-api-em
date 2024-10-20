from http import HTTPStatus
from typing import Any

from httpx import AsyncClient
import pytest
from sqlalchemy import select

from app.core.db import AsyncSessionLocal
from app.models import Product
from app import schemas

from ..conftest import EndpointTestCase
from .conftest import create_product_data

pytestmark = pytest.mark.anyio


class TestCreate(EndpointTestCase):
    NORMAL_REQUEST_DATA = create_product_data('')

    async def test_correct_full_request_creates_product(
        self, async_client: AsyncClient
    ):
        request_data = self.NORMAL_REQUEST_DATA
        response_data = await self._do_request_and_check_response(
            async_client, request_data, HTTPStatus.CREATED
        )
        product_created_data = await self._check_product_created_in_db()
        exp_product_created_data = dict(
            request_data, id=product_created_data['id']
        )
        exp_response_data = exp_product_created_data
        assert product_created_data == exp_product_created_data
        assert response_data == exp_response_data

    async def test_correct_request_without_description_creates_product(
        self, async_client: AsyncClient
    ):
        request_data = dict(self.NORMAL_REQUEST_DATA)
        del request_data['description']
        response_data = await self._do_request_and_check_response(
            async_client, request_data, HTTPStatus.CREATED
        )
        product_created_data = await self._check_product_created_in_db()
        exp_product_created_data = dict(
            request_data, id=product_created_data['id']
        )
        exp_response_data = exp_product_created_data
        assert product_created_data == exp_product_created_data
        assert response_data == exp_response_data

    @pytest.mark.parametrize(
        'invalid_attribute',
        [
            dict(price=-1),
            dict(amount=-1),
            dict(name=''),
            dict(name='a'*257),
        ],
        ids=['price < 0', 'amount < 0', 'empty name', 'name length > 256']
    )
    async def test_request_with_invalid_attribute_fails(
        self, invalid_attribute: dict[str, Any], async_client: AsyncClient
    ):
        request_data = dict(self.NORMAL_REQUEST_DATA, **invalid_attribute)
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
        request_data = dict(self.NORMAL_REQUEST_DATA)
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
    ) -> Any:
        response = await super()._do_request_and_check_response(
            async_client, 'post', '/products', exp_status, json=request_data
        )
        return response.json()

    async def _check_product_created_in_db(self) -> dict[str, Any]:
        async with AsyncSessionLocal() as session:
            sqla_result = await session.scalars(select(Product))
            products_in_db = sqla_result.all()
            assert len(products_in_db) == 1
            product_created = products_in_db[0]
            return schemas.FullProduct.model_validate(
                product_created, from_attributes=True
            ).model_dump(exclude_none=True)

    async def _check_product_not_created_in_db(self) -> None:
        async with AsyncSessionLocal() as session:
            sqla_result = await session.scalars(select(Product))
            products_in_db = sqla_result.all()
            assert len(products_in_db) == 0
