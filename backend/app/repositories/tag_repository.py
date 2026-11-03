from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncConnection


class TagRepository:
    def __init__(self, conn: AsyncConnection) -> None:
        self._conn = conn

    async def get_or_create(self, name: str) -> int:
        name = name.strip().lower()
        row = (
            await self._conn.execute(text("SELECT id FROM tag WHERE name = :name"), {"name": name})
        ).first()
        if row:
            return row[0]
        result = await self._conn.execute(
            text("INSERT INTO tag (name) VALUES (:name)"), {"name": name}
        )
        return result.lastrowid

    async def list_names(self) -> list[str]:
        rows = (await self._conn.execute(text("SELECT name FROM tag ORDER BY name"))).all()
        return [row[0] for row in rows]
