from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.utils.logger import logger
from .custom_exceptions import CustomAPIException


async def api_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, CustomAPIException):
        logger.error(
            "CustomAPIException | {} {} | [{}] {}",
            request.method,
            request.url.path,
            exc.error_code,
            exc.message,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.error_code, "detail": exc.message},
        )

    if isinstance(exc, RequestValidationError):
        first = exc.errors()[0] if exc.errors() else {}
        message = first.get("msg", "Invalid request payload")
        field = " → ".join(str(loc) for loc in first.get("loc", []))
        logger.warning(
            "ValidationError | {} {} | field={} msg={}",
            request.method,
            request.url.path,
            field,
            message,
        )
        return JSONResponse(
            status_code=422,
            content={"error": "VALIDATION_ERROR", "detail": message, "field": field},
        )

    logger.exception("Unhandled exception | {} {}", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"error": "INTERNAL_ERROR", "detail": "An unexpected error occurred"},
    )
