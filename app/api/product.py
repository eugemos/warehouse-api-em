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
    response_model=list[schemas.CreateProductResponse],
    response_model_exclude_none=True,
)
async def list_products(
    product_service: ProductService = Depends(ProductService),
) -> list[models.Product]:
    return await product_service.get_all()
