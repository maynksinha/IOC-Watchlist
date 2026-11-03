from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine

from app.connections import env_config

engine = create_async_engine(
    env_config.DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False},
)


# Raw DDL — single source of truth for the schema (no ORM).
_SCHEMA: tuple[str, ...] = (
    """
    CREATE TABLE IF NOT EXISTS ioc (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        ioc_type      TEXT NOT NULL,
        ioc_raw       TEXT NOT NULL,
        ioc_canonical TEXT NOT NULL UNIQUE,
        note          TEXT,
        created_at    TEXT NOT NULL DEFAULT (datetime('now'))
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS tag (
        id   INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ioc_tag (
        ioc_id INTEGER NOT NULL REFERENCES ioc(id) ON DELETE CASCADE,
        tag_id INTEGER NOT NULL REFERENCES tag(id) ON DELETE CASCADE,
        PRIMARY KEY (ioc_id, tag_id)
    )
    """,
)


async def init_db() -> None:
    async with engine.begin() as conn:
        for statement in _SCHEMA:
            await conn.execute(text(statement))


async def get_db():
    """Yields a connection; commits on success, rolls back on error."""
    async with engine.connect() as conn:
        try:
            yield conn
            await conn.commit()
        except Exception:
            await conn.rollback()
            raise
