from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncConnection

from app.connections.database import get_db
from app.schemas import IOCCreate, api_success
from app.services import IOCService
from app.utils.limiter import limiter
from app.constants import (
    APIPrefix,
    APITag,
    RATE_LIMIT_WRITE,
    PAGINATION_DEFAULT_PAGE,
    PAGINATION_DEFAULT_SIZE,
    PAGINATION_MAX_SIZE,
)

router = APIRouter(prefix=APIPrefix.IOCS.value, tags=[APITag.IOCS.value])


@router.post("", status_code=201)
@limiter.limit(RATE_LIMIT_WRITE)
async def create_ioc(request: Request, body: IOCCreate, db: AsyncConnection = Depends(get_db)):
    ioc = await IOCService(db).create(body)
    return api_success(data=ioc, message="IOC created successfully")


@router.get("")
async def list_iocs(
    type: str | None = Query(None),
    tag: str | None = Query(None),
    page: int = Query(PAGINATION_DEFAULT_PAGE, ge=1),
    size: int = Query(PAGINATION_DEFAULT_SIZE, ge=1, le=PAGINATION_MAX_SIZE),
    db: AsyncConnection = Depends(get_db),
):
    data = await IOCService(db).list(ioc_type=type, tag=tag, page=page, size=size)
    return api_success(data=data, message="IOCs fetched successfully")


@router.delete("/{ioc_id}")
@limiter.limit(RATE_LIMIT_WRITE)
async def delete_ioc(request: Request, ioc_id: int, db: AsyncConnection = Depends(get_db)):
    await IOCService(db).delete(ioc_id)
    return api_success(data={"id": ioc_id}, message="IOC deleted successfully")
