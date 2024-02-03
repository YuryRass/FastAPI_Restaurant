import uuid
from typing import Any

from sqlalchemy import ScalarSelect, Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.dao.base import BaseDAO
from app.database.database import async_session
from app.dish.model import Dish
from app.menu.model import Menu
from app.submenu.model import Submenu


class MenuDAO(BaseDAO):
    model = Menu
    menu_alias = aliased(Menu)
    submenu_alias = aliased(Submenu)
    dish_alias = aliased(Dish)

    @classmethod
    async def show_all(cls) -> list[Menu]:
        """Отображение всех меню."""
        session: AsyncSession
        async with async_session() as session:
            res = await cls.__get_menus_info(session)

            return res

    @classmethod
    async def show(
        cls,
        menu_id: uuid.UUID,
    ) -> Menu:
        """Отображение определенного меню."""
        session: AsyncSession
        async with async_session() as session:
            res = await cls.__get_menu_info(session, menu_id)

            return res

    @classmethod
    async def __get_menu_info(
        cls,
        session: AsyncSession,
        menu_id: uuid.UUID,
    ) -> Menu:
        """Получение информации о конкретном меню."""
        menus_query = cls.__get_menus_query().having(cls.menu_alias.id == menu_id)
        menus = await session.execute(menus_query)
        res = menus.mappings().all()
        if res:
            return res[0]

        return res

    @classmethod
    async def __get_menus_info(cls, session: AsyncSession) -> list[Menu]:
        """Получение информации о всех меню."""
        menus_query = cls.__get_menus_query()
        menus = await session.execute(menus_query)
        res = menus.mappings().all()

        return res

    @classmethod
    def __get_menus_query(cls) -> Select[tuple[uuid.UUID, str, str | None, Any, Any]]:
        """Получение запроса о выводе меню."""
        submenus_count_subq = cls.__get_submenus_count()
        dishes_count_subq = cls.__get_dishes_count()
        return select(
            cls.menu_alias.id,
            cls.menu_alias.title,
            cls.menu_alias.description,
            submenus_count_subq.label('submenus_count'),
            dishes_count_subq.label('dishes_count'),
        ).group_by(cls.menu_alias.id)

    @classmethod
    def __get_submenus_count(cls) -> ScalarSelect:
        """Получение количества подменю."""
        return (
            select(func.count())
            .select_from(cls.submenu_alias)
            .where(cls.submenu_alias.menu_id == cls.menu_alias.id)
            .as_scalar()
        )

    @classmethod
    def __get_dishes_count(cls) -> ScalarSelect:
        """Получение количества блюд."""
        return (
            select(func.count())
            .select_from(cls.dish_alias)
            .join(cls.submenu_alias, cls.dish_alias.submenu)
            .where(cls.submenu_alias.menu_id == cls.menu_alias.id)
            .as_scalar()
        )
