from sqlalchemy.ext.asyncio import AsyncConnection

from app.repositories import TagRepository


class TagService:
    def __init__(self, conn: AsyncConnection) -> None:
        self._repo = TagRepository(conn)

    async def list_tags(self) -> list[str]:
        return await self._repo.list_names()
