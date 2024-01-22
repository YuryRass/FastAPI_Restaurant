from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao.base import BaseDAO
from app.database import async_session
from app.dish.model import Dish
from app.menu.model import Menu
from app.submenu.model import Submenu


class MenuDAO(BaseDAO):
    model = Menu

    @classmethod
    async def show(cls, **kwargs):
        # вывод таблицы menu и подсчет кол-ва подменю
        stmt1 = (
            select(
                Menu.id,
                Menu.title,
                Menu.description,
                func.count(Submenu.menu_id)
                .filter(Submenu.menu_id.is_not(None))
                .label("submenus_count"),
            )
            .select_from(Menu)
            .filter_by(**kwargs)
            .join(Submenu, Menu.id == Submenu.menu_id, isouter=True)
            .group_by(Menu.id, Submenu.menu_id)
        )

        # подсчет кол-ва блюд для меню
        stmt2 = (
            select(
                func.count(Dish.submenu_id)
                .filter(Dish.submenu_id.is_not(None))
                .label("dishes_count"),
            )
            .select_from(Menu)
            .filter_by(**kwargs)
            .join(Submenu, Menu.id == Submenu.menu_id, isouter=True)
            .join(Dish, Submenu.id == Dish.submenu_id, isouter=True)
            .group_by(Dish.submenu_id)
        )

        session: AsyncSession
        async with async_session() as session:
            res = await cls.__unioned_result(session, stmt1, stmt2)
            if kwargs and res:
                return res[0]
            return res

    @classmethod
    async def __unioned_result(cls, session: AsyncSession, stmt1, stmt2):
        result1 = await session.execute(stmt1)
        result2 = await session.execute(stmt2)
        res1 = result1.mappings().all()
        res2 = result2.mappings().all()
        return [dict(**r1, **r2) for r1, r2 in zip(res1, res2)]
