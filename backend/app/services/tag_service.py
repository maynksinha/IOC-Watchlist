from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import TagRepository


class TagService:
    def __init__(self, db: AsyncSession) -> None:
        self._repo = TagRepository(db)

    async def list_tags(self) -> list[str]:
        return await self._repo.list_names()
