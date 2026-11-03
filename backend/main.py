import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.connections import env_config
from app.connections.database import engine, Base
from app.controllers import include_routes
from app.exceptions import CustomAPIException, api_exception_handler
from app.constants import AppDefault
from app.utils.logger import logger


@asynccontextmanager
async def lifespan(_app: FastAPI):
    if "sqlite" in env_config.DATABASE_URL:
        Path(env_config.DATABASE_URL.split("///")[-1]).parent.mkdir(parents=True, exist_ok=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Server started | ENV={} | {}:{}", env_config.ENV, env_config.HOST, env_config.PORT)
    yield
    logger.info("Server shutting down")


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

    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        log = logger.success if response.status_code < 400 else logger.error
        log(
            "{} {} | status={} | {:.1f}ms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response

    app.add_exception_handler(Exception, api_exception_handler)

    include_routes(app)

    dist_dir = Path(__file__).parent.parent / "frontend" / "dist"
    if dist_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(dist_dir / "assets")), name="assets")

        @app.get("/{full_path:path}", include_in_schema=False)
        async def spa_fallback(full_path: str):
            return FileResponse(str(dist_dir / "index.html"))

    return app
