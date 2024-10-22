from typing import Annotated

from pydantic import BaseModel, Field, RootModel

from app.core.constants import MAX_PRODUCT_NAME_LENGTH

ProductId = Annotated[
    int,
    Field(
        title='Идентификатор',
        description='Идентификатор товара',
        examples=[1]
    ),
]

ProductName = Annotated[
    str,
    Field(
        min_length=1,
        max_length=MAX_PRODUCT_NAME_LENGTH,
        title='Наименование',
        description='Наименование товара',
        examples=['Велосипед']
    ),
]

ProductDescription = Annotated[
    str | None,
    Field(
        title='Описание',
        description='Описание товара',
        examples=['Велосипед складной, синий']
    )
]

ProductPrice = Annotated[
    int,
    Field(
        ge=0,
        title='Цена',
        description='Цена товара',
        examples=['1000']
    )
]
ProductAmount = Annotated[
    int,
    Field(
        ge=0,
        title='Количество',
        description='Количество товара на складе',
        examples=['100']
    )
]


class BaseProduct(BaseModel):
    """Базовая информация о товаре"""
    name: ProductName
    description: ProductDescription = None
    price: ProductPrice
    amount: ProductAmount


class FullProduct(BaseProduct):
    """Полная информация о товаре"""
    id: ProductId


class CreateProductRequest(BaseProduct):
    """Запрос на создание товара"""
    pass


class CreateProductResponse(FullProduct):
    """Отет на запрос на создание товара"""
    pass


class ListProductsResponse(RootModel):
    """Ответ на запрос о получении списка товаров"""
    root: list[FullProduct]


class GetProductResponse(BaseProduct):
    """Ответ на запрос о получении информации о товаре"""
    pass


class UpdateProductRequest(BaseModel):
    """Запрос на изменение информации о товаре"""
    name: ProductName | None = None
    description: ProductDescription = None
    price: ProductPrice | None = None
    amount: ProductAmount | None = None

    model_config = dict(extra='forbid')


class UpdateProductResponse(BaseProduct):
    """Ответ на запрос на изменение информации о товаре"""
    pass
