from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Tag


class TagRepository:
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_name(self, name: str) -> Tag | None:
        result = await self._db.execute(select(Tag).where(Tag.name == name))
        return result.scalar_one_or_none()

    async def create(self, name: str) -> Tag:
        tag = Tag(name=name)
        self._db.add(tag)
        await self._db.flush()
        return tag

    async def get_or_create(self, name: str) -> Tag:
        name = name.strip().lower()
        tag = await self.get_by_name(name)
        if not tag:
            tag = await self.create(name)
        return tag

    async def list_names(self) -> list[str]:
        result = await self._db.execute(select(Tag.name).order_by(Tag.name))
        return [row[0] for row in result.all()]
