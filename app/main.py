from fastapi import FastAPI

from app.api import router
from app.core.config import settings
from app.exceptions import add_error_handlers

app = FastAPI(title=settings.app_title)
app.include_router(router)
add_error_handlers(app)
