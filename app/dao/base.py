"""Основной DAO (Data Access Object)."""

import uuid
from typing import Generic

from sqlalchemy import delete, insert, select, update
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import ModelType
from app.database.database import async_engine, async_session


class BaseDAO(Generic[ModelType]):
    """Класс, описывающий основные CRUD операции для моделей."""

    model: type[ModelType]

    @classmethod
    async def get_by_id(cls, model_id: uuid.UUID) -> RowMapping | None:
        """Получение записи в модели по ее ID."""
        session: AsyncSession
        async with async_session() as session:
            stmt = select(cls.model.__table__.columns).where(cls.model.id == model_id)
            result = await session.execute(stmt)
            return result.mappings().one_or_none()

    @classmethod
    async def add(cls, **data) -> RowMapping:
        """Добавление записи в модель."""
        assert cls.model is not None
        stmt = insert(cls.model).values(**data).returning(cls.model.id)
        session: AsyncSession
        async with async_session() as session:
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().one()

    @classmethod
    async def get_identifiers(cls, **kwargs) -> list[uuid.UUID]:
        """Получение всех ID модели."""
        assert cls.model is not None
        stmt = select(cls.model.id).select_from(cls.model).filter_by(**kwargs)
        async with async_engine.connect() as conn:
            result = await conn.execute(stmt)
            return result.scalars().fetchall()

    @classmethod
    async def update(cls, model_id: uuid.UUID, **data) -> RowMapping:
        """Изменение записи в модели."""
        assert cls.model is not None
        stmt = (
            update(cls.model)
            .where(cls.model.id == model_id)
            .values(**data)
            .returning(cls.model.__table__.columns)
        )
        session: AsyncSession
        async with async_session() as session:
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().one()

    @classmethod
    async def delete_record(cls, **kwargs) -> RowMapping | None:
        """Удаление записи из модели."""
        assert cls.model is not None
        stmt = delete(cls.model).filter_by(**kwargs).returning(cls.model.id)

        session: AsyncSession
        async with async_session() as session:
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().one_or_none()
