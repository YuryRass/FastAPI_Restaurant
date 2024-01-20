import uuid
from sqlalchemy import distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.database import async_session
from app.dish.model import Dish
from app.menu.model import Menu
from app.submenu.model import Submenu


class MenuDAO(BaseDAO):
    model = Menu

    @classmethod
    async def show_menu(cls, **kwargs):
        stmt = (
            select(
                Menu.id,
                Menu.title,
                Menu.description,
                func.count(distinct(Dish.submenu_id))
                .filter(Dish.submenu_id.is_not(None))
                .label("submenus_count"),
                func.count(Dish.submenu_id)
                .filter(Dish.submenu_id.is_not(None))
                .label("dishes_count"),
            )
            .select_from(Menu)
            .filter_by(**kwargs)
            .join(Submenu, Menu.id == Submenu.menu_id, isouter=True)
            .join(Dish, Submenu.id == Dish.submenu_id, isouter=True)
            .group_by(Menu.id, Dish.submenu_id)
        )

        session: AsyncSession
        async with async_session() as session:
            result = await session.execute(stmt)
            await session.commit()
            if kwargs:
                return result.mappings().one_or_none()
            return result.mappings().all()

    @classmethod
    async def update_menu(cls, menu_id: uuid.UUID, **data):
        updated_menu: Menu = super().update(menu_id, **data)
        menu_res = await cls.show_menu(id=updated_menu.id)
        return menu_res
