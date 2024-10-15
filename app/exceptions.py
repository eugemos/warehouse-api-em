from http import HTTPStatus

from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler
from sqlalchemy.orm.exc import NoResultFound


async def object_not_found_error_handler(request, exc):
    return await http_exception_handler(
        request, HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Объект не найден!'
        )
    )


def add_error_handlers(app: FastAPI) -> None:
    app.exception_handler(NoResultFound)(object_not_found_error_handler)
