from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.ioc_engine import normalize_and_detect, InvalidIOCError
from app.repositories import IOCRepository, TagRepository
from app.schemas import IOCCreate
from app.models import IOC


@dataclass
class CreateResult:
    ioc: IOC | None
    canonical: str
    duplicate: bool


class IOCService:
    def __init__(self, db: AsyncSession) -> None:
        self._ioc_repo = IOCRepository(db)
        self._tag_repo = TagRepository(db)

    def normalize(self, raw: str) -> tuple[str, object]:
        """Raises InvalidIOCError when the value cannot be classified."""
        return normalize_and_detect(raw)

    async def create(self, data: IOCCreate) -> CreateResult:
        canonical, ioc_type = normalize_and_detect(data.value)

        tags = []
        for tag_name in data.tags:
            if tag_name.strip():
                tag = await self._tag_repo.get_or_create(tag_name)
                tags.append(tag)

        ioc = await self._ioc_repo.create(
            ioc_type=ioc_type,
            ioc_raw=data.value.strip(),
            ioc_canonical=canonical,
            note=data.note,
            tags=tags,
        )
        return CreateResult(ioc=ioc, canonical=canonical, duplicate=(ioc is None))

    async def get_by_canonical(self, canonical: str) -> IOC | None:
        return await self._ioc_repo.get_by_canonical(canonical)

    async def list(
        self,
        ioc_type: str | None = None,
        tag: str | None = None,
        page: int = 1,
        size: int = 50,
    ) -> tuple[int, list[IOC]]:
        return await self._ioc_repo.list(ioc_type=ioc_type, tag=tag, page=page, size=size)

    async def delete(self, ioc_id: int) -> bool:
        ioc = await self._ioc_repo.get_by_id(ioc_id)
        if not ioc:
            return False
        await self._ioc_repo.delete(ioc)
        return True
