from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.connections.database import get_db
from app.schemas import IOCCreate, IOCResponse, IOCListResponse
from app.services import IOCService
from app.exceptions import CustomAPIException
from app.utils.ioc_engine import InvalidIOCError
from app.utils.logger import logger
from app.constants import (
    APIPrefix,
    APITag,
    ErrorCode,
    PAGINATION_DEFAULT_PAGE,
    PAGINATION_DEFAULT_SIZE,
    PAGINATION_MAX_SIZE,
)

router = APIRouter(prefix=APIPrefix.IOCS.value, tags=[APITag.IOCS.value])


@router.post("", status_code=201, response_model=IOCResponse)
async def create_ioc(body: IOCCreate, db: AsyncSession = Depends(get_db)):
    service = IOCService(db)

    try:
        service.normalize(body.value)
    except InvalidIOCError as exc:
        raise CustomAPIException(str(exc), error_code=ErrorCode.INVALID_IOC, status_code=400)

    result = await service.create(body)

    if result.duplicate:
        existing = await service.get_by_canonical(result.canonical)
        raise CustomAPIException(
            f"IOC already exists with id={existing.id}",
            error_code=ErrorCode.DUPLICATE_IOC,
            status_code=409,
        )

    logger.success("IOC created | id={} type={} canonical={}", result.ioc.id, result.ioc.ioc_type, result.ioc.ioc_canonical)
    return result.ioc


@router.get("", response_model=IOCListResponse)
async def list_iocs(
    type: str | None = Query(None),
    tag: str | None = Query(None),
    page: int = Query(PAGINATION_DEFAULT_PAGE, ge=1),
    size: int = Query(PAGINATION_DEFAULT_SIZE, ge=1, le=PAGINATION_MAX_SIZE),
    db: AsyncSession = Depends(get_db),
):
    service = IOCService(db)
    total, items = await service.list(ioc_type=type, tag=tag, page=page, size=size)
    logger.success("IOC list | total={} page={} size={}", total, page, size)
    return {"total": total, "page": page, "size": size, "items": items}


@router.delete("/{ioc_id}", status_code=204)
async def delete_ioc(ioc_id: int, db: AsyncSession = Depends(get_db)):
    service = IOCService(db)
    deleted = await service.delete(ioc_id)
    if not deleted:
        raise CustomAPIException(
            f"IOC {ioc_id} not found",
            error_code=ErrorCode.NOT_FOUND,
            status_code=404,
        )
    logger.success("IOC deleted | id={}", ioc_id)
