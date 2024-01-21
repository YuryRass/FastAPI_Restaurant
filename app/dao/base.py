"""Основной DAO (Data Access Object)"""
import uuid

from sqlalchemy import delete, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, **data):
        stmt = insert(cls.model).values(**data).returning(cls.model.id)
        session: AsyncSession
        async with async_session() as session:
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().one()

    @classmethod
    async def update(cls, model_id: uuid.UUID, **data):
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
    async def delete_record(cls, **kwargs):
        stmt = delete(cls.model).filter_by(**kwargs).returning(cls.model.id)

        session: AsyncSession
        async with async_session() as session:
            result = await session.execute(stmt)
            await session.commit()
            return result.mappings().one_or_none()
