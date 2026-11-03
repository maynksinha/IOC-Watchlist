from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from app.models import IOC, Tag
from app.constants import IOCType


class IOCRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_canonical(self, canonical: str) -> IOC | None:
        result = await self._db.execute(select(IOC).where(IOC.ioc_canonical == canonical))
        return result.scalar_one_or_none()

    async def get_by_id(self, ioc_id: int) -> IOC | None:
        result = await self._db.execute(select(IOC).where(IOC.id == ioc_id))
        return result.scalar_one_or_none()

    async def create(
        self,
        ioc_type: IOCType,
        ioc_raw: str,
        ioc_canonical: str,
        note: str | None,
        tags: list,
    ) -> IOC | None:
        ioc = IOC(
            ioc_type=ioc_type.value,
            ioc_raw=ioc_raw,
            ioc_canonical=ioc_canonical,
            note=note,
            tags=tags,
        )
        self._db.add(ioc)
        try:
            await self._db.commit()
            await self._db.refresh(ioc)
            return ioc
        except IntegrityError:
            await self._db.rollback()
            return None

    async def list(
        self,
        ioc_type: str | None = None,
        tag: str | None = None,
        page: int = 1,
        size: int = 50,
    ) -> tuple[int, list[IOC]]:
        query = select(IOC)
        if ioc_type:
            query = query.where(IOC.ioc_type == ioc_type)
        if tag:
            query = query.join(IOC.tags).where(Tag.name == tag.lower())

        count_q = select(func.count()).select_from(query.subquery())
        total = (await self._db.execute(count_q)).scalar_one()

        query = query.order_by(IOC.created_at.desc()).offset((page - 1) * size).limit(size)
        result = await self._db.execute(query)
        items = result.scalars().unique().all()
        return total, list(items)

    async def delete(self, ioc: IOC) -> None:
        await self._db.delete(ioc)
        await self._db.commit()
