from http import HTTPStatus

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
        response_data = await self._send_request(async_client, request_data)
        product_created_data = await self._check_product_created_in_db()
        exp_response_data = dict(request_data, id=product_created_data['id'])
        assert exp_response_data == product_created_data
        assert exp_response_data == response_data

    # async def test_correct_request_without_description_creates_product():
    #     ...

    # async def test_request_with_negative_price_fails(self, ):
    #     ...

    # async def test_request_with_negative_amount_fails(self, ):
    #     ...

    # async def test_request_with_empty_name_fails(self, ):
    #     ...

    # async def test_request_without_name_fails(self, ):
    #     ...

    # async def test_request_without_price_fails(self, ):
    #     ...

    # async def test_request_without_amount_fails(self, ):
    #     ...

    async def _send_request(
        self, async_client: AsyncClient, request_data: dict
    ):
        async with async_client as client:
            response = await client.post("/products", json=request_data)

        assert response.status_code == HTTPStatus.CREATED
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
