from fastapi import APIRouter

from .order import router as orders_router
from .product import router as products_router

router = APIRouter()
router.include_router(orders_router, prefix='/orders')
router.include_router(products_router, prefix='/products')
