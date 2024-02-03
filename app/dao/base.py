"""Основной DAO (Data Access Object)."""
import uuid
from typing import Generic, TypeVar

from sqlalchemy import delete, insert, update
from sqlalchemy.engine.row import RowMapping
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import async_session
from app.dish.model import Dish
from app.menu.model import Menu
from app.submenu.model import Submenu

ModelType = TypeVar('ModelType', Dish, Menu, Submenu)


class BaseDAO(Generic[ModelType]):
    """Класс, описывающий основные CRUD операции для моделей."""
    model: type[ModelType]

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
