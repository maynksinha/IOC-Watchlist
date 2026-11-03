from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncConnection

from app.connections.database import get_db
from app.schemas import api_success
from app.services import TagService
from app.constants import APIPrefix, APITag

router = APIRouter(prefix=APIPrefix.TAGS.value, tags=[APITag.TAGS.value])


@router.get("")
async def list_tags(db: AsyncConnection = Depends(get_db)):
    tags = await TagService(db).list_tags()
    return api_success(data=tags, message="Tags fetched successfully")
