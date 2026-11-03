from fastapi import FastAPI

from .health_controller import router as health_router
from .ioc_controller import router as ioc_router
from .tag_controller import router as tag_router

_routers = (
    health_router,
    ioc_router,
    tag_router,
)


def include_routes(app: FastAPI) -> None:
    for router in _routers:
        app.include_router(router)
