from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas.response import api_error
from app.utils.logger import logger
from .custom_exceptions import CustomAPIException


async def custom_api_exception_handler(request: Request, exc: CustomAPIException) -> JSONResponse:
    log = logger.warning if exc.status_code < 500 else logger.error
    log("{} {} | {} | {}", request.method, request.url.path, exc.error_code, exc.message)
    return JSONResponse(
        status_code=exc.status_code,
        content=api_error(exc.message, exc.error_code),
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    first = exc.errors()[0] if exc.errors() else {}
    field = " → ".join(str(loc) for loc in first.get("loc", []) if loc != "body")
    message = first.get("msg", "Invalid request payload")
    detail = f"{field}: {message}" if field else message
    logger.warning("{} {} | VALIDATION_ERROR | {}", request.method, request.url.path, detail)
    return JSONResponse(
        status_code=422,
        content=api_error(detail, "VALIDATION_ERROR"),
    )
