from __future__ import annotations

from sqlalchemy import text, bindparam
from sqlalchemy.ext.asyncio import AsyncConnection

_COLUMNS = "id, ioc_type, ioc_raw, ioc_canonical, note, created_at"


class IOCRepository:
    def __init__(self, conn: AsyncConnection) -> None:
        self._conn = conn

    async def get_by_canonical(self, canonical: str) -> dict | None:
        row = (
            await self._conn.execute(
                text(f"SELECT {_COLUMNS} FROM ioc WHERE ioc_canonical = :canonical"),
                {"canonical": canonical},
            )
        ).mappings().first()
        return dict(row) if row else None

    async def get_by_id(self, ioc_id: int) -> dict | None:
        row = (
            await self._conn.execute(
                text(f"SELECT {_COLUMNS} FROM ioc WHERE id = :id"),
                {"id": ioc_id},
            )
        ).mappings().first()
        if not row:
            return None
        ioc = dict(row)
        ioc["tags"] = (await self._tags_for([ioc_id])).get(ioc_id, [])
        return ioc

    async def insert(self, ioc_type: str, ioc_raw: str, canonical: str, note: str | None) -> int:
        result = await self._conn.execute(
            text(
                "INSERT INTO ioc (ioc_type, ioc_raw, ioc_canonical, note, created_at) "
                "VALUES (:type, :raw, :canonical, :note, datetime('now'))"
            ),
            {"type": ioc_type, "raw": ioc_raw, "canonical": canonical, "note": note},
        )
        return result.lastrowid

    async def link_tags(self, ioc_id: int, tag_ids: list[int]) -> None:
        for tag_id in tag_ids:
            await self._conn.execute(
                text("INSERT OR IGNORE INTO ioc_tag (ioc_id, tag_id) VALUES (:ioc_id, :tag_id)"),
                {"ioc_id": ioc_id, "tag_id": tag_id},
            )

    async def list(
        self,
        ioc_type: str | None = None,
        tag: str | None = None,
        page: int = 1,
        size: int = 50,
    ) -> tuple[int, list[dict]]:
        join = ""
        where: list[str] = []
        params: dict = {}

        if ioc_type:
            where.append("i.ioc_type = :ioc_type")
            params["ioc_type"] = ioc_type
        if tag:
            join = "JOIN ioc_tag it ON it.ioc_id = i.id JOIN tag t ON t.id = it.tag_id"
            where.append("t.name = :tag")
            params["tag"] = tag.lower()

        where_sql = f"WHERE {' AND '.join(where)}" if where else ""

        total = (
            await self._conn.execute(
                text(f"SELECT COUNT(DISTINCT i.id) FROM ioc i {join} {where_sql}"),
                params,
            )
        ).scalar_one()

        rows = (
            await self._conn.execute(
                text(
                    f"SELECT DISTINCT i.id, i.ioc_type, i.ioc_raw, i.ioc_canonical, i.note, i.created_at "
                    f"FROM ioc i {join} {where_sql} "
                    f"ORDER BY i.created_at DESC, i.id DESC "
                    f"LIMIT :limit OFFSET :offset"
                ),
                {**params, "limit": size, "offset": (page - 1) * size},
            )
        ).mappings().all()

        items = [dict(r) for r in rows]
        tags_map = await self._tags_for([item["id"] for item in items])
        for item in items:
            item["tags"] = tags_map.get(item["id"], [])
        return total, items

    async def delete(self, ioc_id: int) -> None:
        await self._conn.execute(text("DELETE FROM ioc_tag WHERE ioc_id = :id"), {"id": ioc_id})
        await self._conn.execute(text("DELETE FROM ioc WHERE id = :id"), {"id": ioc_id})

    async def _tags_for(self, ioc_ids: list[int]) -> dict[int, list[str]]:
        if not ioc_ids:
            return {}
        stmt = text(
            "SELECT it.ioc_id AS ioc_id, t.name AS name "
            "FROM ioc_tag it JOIN tag t ON t.id = it.tag_id "
            "WHERE it.ioc_id IN :ids ORDER BY t.name"
        ).bindparams(bindparam("ids", expanding=True))
        rows = (await self._conn.execute(stmt, {"ids": ioc_ids})).mappings().all()
        result: dict[int, list[str]] = {}
        for row in rows:
            result.setdefault(row["ioc_id"], []).append(row["name"])
        return result
