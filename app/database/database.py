import asyncio
import uuid
from contextlib import asynccontextmanager

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

from app.config import settings

if settings.MODE == 'TEST':
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {'poolclass': NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}


async_engine: AsyncEngine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

async_session_: async_sessionmaker = async_sessionmaker(
    async_engine, expire_on_commit=False
)


@asynccontextmanager
async def async_session():
    scoped_factory = async_scoped_session(
        async_session_,
        scopefunc=asyncio.current_task,
    )
    try:
        async with scoped_factory() as s:
            yield s
    finally:
        await scoped_factory.remove()


class Base(DeclarativeBase):
    """Базовый класс для декларативных определений классов."""

    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
