from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.connections.database import get_db
from app.services import TagService
from app.utils.logger import logger
from app.constants import APIPrefix, APITag

router = APIRouter(prefix=APIPrefix.TAGS.value, tags=[APITag.TAGS.value])


@router.get("", response_model=list[str])
async def list_tags(db: AsyncSession = Depends(get_db)):
    service = TagService(db)
    tags = await service.list_tags()
    logger.success("Tags fetched | count={}", len(tags))
    return tags
