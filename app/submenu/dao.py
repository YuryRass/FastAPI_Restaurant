import uuid
from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.dao.base import BaseDAO
from app.database.database import async_session
from app.dish.model import Dish
from app.submenu.model import Submenu


class SubmenuDAO(BaseDAO):
    """CRUD операции для подменю."""
    model = Submenu
    submenu_alias = aliased(Submenu)
    dish_alias = aliased(Dish)

    @classmethod
    async def show_all(
        cls,
        menu_id: uuid.UUID,
    ) -> list[Submenu]:
        """Отображение списка подменю."""
        session: AsyncSession
        async with async_session() as session:
            result = await cls.__get_submenus_info(
                session,
                menu_id,
            )
            return result

    @classmethod
    async def show(cls, menu_id: uuid.UUID, submenu_id: uuid.UUID) -> Submenu:
        """Отображение подменю."""
        session: AsyncSession
        async with async_session() as session:
            result = await cls.__get_submenu_info(
                session,
                menu_id,
                submenu_id,
            )
            return result

    @classmethod
    async def __get_submenu_info(
        cls,
        session: AsyncSession,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> Submenu:
        """Исполнение запроса об отображении подменю."""
        stmt = cls.__get_submenu_query(menu_id, submenu_id)

        result = await session.execute(stmt)
        submenu_res = result.mappings().all()
        if submenu_res:
            return submenu_res[0]
        return submenu_res

    @classmethod
    async def __get_submenus_info(
        cls,
        session: AsyncSession,
        menu_id: uuid.UUID,
    ) -> list[Submenu]:
        """Исполнение запроса об отображении списка подменю."""
        stmt = cls.__get_submenus_query(menu_id)

        result = await session.execute(stmt)
        submenu_res = result.mappings().all()

        return submenu_res

    @classmethod
    def __get_submenu_query(
        cls,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> Select[tuple[uuid.UUID, str, str | None, Any]]:
        """Запрос на получение подменю."""
        stmt = cls.__get_submenus_query(menu_id)
        stmt = stmt.having(cls.submenu_alias.id == submenu_id)
        return stmt

    @classmethod
    def __get_submenus_query(
        cls,
        menu_id: uuid.UUID,
    ) -> Select[tuple[uuid.UUID, str, str | None, Any]]:
        """Запрос на получение списка подменю"""
        dish_alias = aliased(Dish)

        dishes_count = (
            select(func.count())
            .select_from(cls.submenu_alias)
            .where(cls.submenu_alias.id == dish_alias.submenu_id)
            .as_scalar()
        )

        stmt = (
            select(
                cls.submenu_alias.id,
                cls.submenu_alias.title,
                cls.submenu_alias.description,
                dishes_count.label('dishes_count'),
            )
            .group_by(cls.submenu_alias.id)
            .having(
                cls.submenu_alias.menu_id == menu_id,
            )
        )
        return stmt
