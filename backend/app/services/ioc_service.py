from sqlalchemy.ext.asyncio import AsyncConnection

from app.repositories import IOCRepository, TagRepository
from app.schemas import IOCCreate
from app.exceptions import CustomAPIException
from app.utils.ioc_engine import normalize_and_detect, InvalidIOCError
from app.constants import ErrorCode


class IOCService:
    def __init__(self, conn: AsyncConnection) -> None:
        self._ioc = IOCRepository(conn)
        self._tag = TagRepository(conn)

    async def create(self, data: IOCCreate) -> dict:
        try:
            canonical, ioc_type = normalize_and_detect(data.value)
        except InvalidIOCError as exc:
            raise CustomAPIException(str(exc), ErrorCode.INVALID_IOC, status_code=400) from exc

        existing = await self._ioc.get_by_canonical(canonical)
        if existing:
            raise CustomAPIException(
                f"IOC already exists with id={existing['id']}",
                ErrorCode.DUPLICATE_IOC,
                status_code=409,
            )

        tag_ids = [await self._tag.get_or_create(name) for name in data.tags if name.strip()]
        ioc_id = await self._ioc.insert(ioc_type.value, data.value.strip(), canonical, data.note)
        await self._ioc.link_tags(ioc_id, tag_ids)
        return await self._ioc.get_by_id(ioc_id)

    async def list(
        self,
        ioc_type: str | None = None,
        tag: str | None = None,
        page: int = 1,
        size: int = 50,
    ) -> dict:
        total, items = await self._ioc.list(ioc_type=ioc_type, tag=tag, page=page, size=size)
        return {"total": total, "page": page, "size": size, "items": items}

    async def delete(self, ioc_id: int) -> None:
        if not await self._ioc.get_by_id(ioc_id):
            raise CustomAPIException(f"IOC {ioc_id} not found", ErrorCode.NOT_FOUND, status_code=404)
        await self._ioc.delete(ioc_id)
