from fastapi import APIRouter

from app.utils.logger import logger
from app.constants import APITag

router = APIRouter(tags=[APITag.HEALTH.value])


@router.get("/healthz")
async def health_check():
    logger.success("Health check | OK")
    return {"status": "ok"}
