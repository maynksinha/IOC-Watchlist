import logging
import time
import uvicorn
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from slowapi.errors import RateLimitExceeded

from app.connections import env_config
from app.connections.database import init_db, engine
from app.controllers import include_routes
from app.exceptions import (
    CustomAPIException,
    custom_api_exception_handler,
    validation_exception_handler,
)
from app.schemas import api_error
from app.constants import AppDefault, ErrorCode, MAX_BODY_BYTES
from app.utils.limiter import limiter
from app.utils.logger import logger


async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    logger.warning("{} {} | RATE_LIMITED | too many requests", request.method, request.url.path)
    return JSONResponse(
        status_code=429,
        content=api_error("Too many requests. Please slow down and try again.", ErrorCode.RATE_LIMITED.value),
    )

# Silence uvicorn's own loggers — our loguru handles every line.
logging.getLogger("uvicorn.access").setLevel(logging.CRITICAL)
logging.getLogger("uvicorn.error").setLevel(logging.CRITICAL)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if "sqlite" in env_config.DATABASE_URL:
        Path(env_config.DATABASE_URL.split("///")[-1]).parent.mkdir(parents=True, exist_ok=True)
    await init_db()
    logger.info("Server started | ENV={} | {}:{}", env_config.ENV, env_config.HOST, env_config.PORT)
    yield
    await engine.dispose()
    logger.info("Server stopped")


def create_app() -> FastAPI:
    app = FastAPI(
        title=AppDefault.TITLE.value,
        version=AppDefault.VERSION.value,
        description=AppDefault.DESCRIPTION.value,
        lifespan=lifespan,
        docs_url=None if env_config.IS_PROD else "/docs",
        redoc_url=None if env_config.IS_PROD else "/redoc",
        openapi_url=None if env_config.IS_PROD else "/openapi.json",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=env_config.CORS_ORIGINS_LIST,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.limiter = limiter

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.perf_counter()

        # Reject oversized payloads before touching the route.
        content_length = request.headers.get("content-length")
        if content_length and content_length.isdigit() and int(content_length) > MAX_BODY_BYTES:
            logger.warning("{} {} | 413 | request body too large", request.method, request.url.path)
            return JSONResponse(
                status_code=413,
                content=api_error("Request body too large.", ErrorCode.PAYLOAD_TOO_LARGE.value),
            )

        try:
            response = await call_next(request)
        except Exception:
            elapsed = (time.perf_counter() - start) * 1000
            logger.exception("{} {} | 500 | {:.1f}ms", request.method, request.url.path, elapsed)
            return JSONResponse(
                status_code=500,
                content=api_error("Internal server error", ErrorCode.INTERNAL_ERROR.value),
            )
        elapsed = (time.perf_counter() - start) * 1000
        if response.status_code >= 500:
            log = logger.error
        elif response.status_code >= 400:
            log = logger.warning
        else:
            log = logger.info
        log("{} {} | {} | {:.1f}ms", request.method, request.url.path, response.status_code, elapsed)
        return response

    app.add_exception_handler(CustomAPIException, custom_api_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(RateLimitExceeded, rate_limit_handler)

    include_routes(app)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "run:app",
        host=env_config.HOST,
        port=env_config.PORT,
        reload=not env_config.IS_PROD,
        access_log=False,
    )
