from fastapi import APIRouter

from app.schemas import api_success
from app.constants import APITag

router = APIRouter(tags=[APITag.HEALTH.value])


@router.get("/healthz")
async def health_check():
    return api_success(data={"status": "ok"}, message="Service healthy")
