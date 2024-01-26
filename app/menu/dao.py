import uuid
from sqlalchemy import func, select
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.database import async_session
from app.dish.model import Dish
from app.menu.model import Menu
from app.submenu.model import Submenu


class MenuDAO(BaseDAO):
    model = Menu

    @classmethod
    async def show(cls, menu_id: uuid.UUID | None = None):
        session: AsyncSession
        async with async_session() as session:
            res = await cls.__get_menu_info(session, menu_id)
            if menu_id and res:
                return res[0]

            return res

    @classmethod
    async def __get_menu_info(
        cls,
        session: AsyncSession,
        menu_id: uuid.UUID | None = None,
    ):
        menu_alias = aliased(Menu)
        submenu_alias = aliased(Submenu)
        dish_alias = aliased(Dish)

        submenus_count_subq = (
            select(func.count())
            .select_from(submenu_alias)
            .where(submenu_alias.menu_id == menu_alias.id)
            .as_scalar()
        )

        dishes_count_subq = (
            select(func.count())
            .select_from(dish_alias)
            .join(submenu_alias, dish_alias.submenu)
            .where(submenu_alias.menu_id == menu_alias.id)
            .as_scalar()
        )

        menus_query = (
            select(
                menu_alias.id,
                menu_alias.title,
                menu_alias.description,
                submenus_count_subq.label("submenus_count"),
                dishes_count_subq.label("dishes_count"),
            )
            .group_by(menu_alias.id)
        )

        if menu_id:
            menus_query = menus_query.having(menu_alias.id == menu_id)

        menus = await session.execute(menus_query)
        return menus.mappings().all()
