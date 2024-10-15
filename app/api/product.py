from http import HTTPStatus

from fastapi import APIRouter, Depends

from app import models
from app import schemas
from app.services import ProductService

router = APIRouter()


@router.post(
    '',
    response_model=schemas.CreateProductResponse,
    response_model_exclude_none=True,
)
async def create_product(
    request_body: schemas.CreateProductRequest,
    product_service: ProductService = Depends(ProductService),
) -> models.Product:
    return await product_service.create(request_body)


@router.get(
    '',
    response_model=schemas.ListProductsResponse,
    response_model_exclude_none=True,
)
async def list_products(
    product_service: ProductService = Depends(ProductService),
) -> list[models.Product]:
    return await product_service.get_all()


@router.get(
    '/{id}',
    response_model=schemas.GetProductResponse,
    response_model_exclude_none=True,
)
async def get_product(
    id: int,
    product_service: ProductService = Depends(ProductService),
) -> models.Product:
    return await product_service.get_or_error(id)


@router.put(
    '/{id}',
    response_model=schemas.UpdateProductResponse,
    response_model_exclude_none=True,
)
async def update_product(
    id: int,
    request_body: schemas.UpdateProductRequest,
    product_service: ProductService = Depends(ProductService),
) -> models.Product:
    return await product_service.update(id, request_body)


@router.delete(
    '/{id}',
    response_model=None,
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_product(
    id: int,
    product_service: ProductService = Depends(ProductService),
) -> None:
    return await product_service.delete(id)
