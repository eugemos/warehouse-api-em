import pytest
from sqlalchemy import insert

from app.core.db import AsyncSessionLocal
from app.models import Product

FIXTURE_PRODUCTS_COUNT = 3


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
        create_product_data(i, id=i)
        for i in range(1, FIXTURE_PRODUCTS_COUNT + 1)
    ]
    del data[1]['description']
    return data


@pytest.fixture
async def create_products_in_db():
    products_data = create_fixture_products_data()
    async with AsyncSessionLocal() as session:
        await session.execute(insert(Product), products_data)
        await session.commit()
