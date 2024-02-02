import uuid

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.dao.base import BaseDAO
from app.database import async_session
from app.dish.model import Dish
from app.submenu.model import Submenu


class DishDAO(BaseDAO):
    model = Dish

    @classmethod
    async def show(
        cls,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID | None = None,
    ) -> Dish:
        session: AsyncSession
        async with async_session() as session:
            res: Dish = await cls.__get_dish_info(
                session,
                menu_id,
                submenu_id,
                dish_id,
            )
            return res

    @classmethod
    async def __get_dish_info(
        cls,
        session: AsyncSession,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID | None = None,
    ) -> Dish:
        dish_alias = aliased(Dish)
        submenu_alias = aliased(Submenu)
        stmt = (
            select(
                dish_alias.id,
                dish_alias.title,
                dish_alias.description,
                dish_alias.price,
            )
            .select_from(dish_alias)
            .where(
                and_(
                    submenu_alias.menu_id == menu_id,
                    dish_alias.submenu_id == submenu_id,
                )
            )
            .join(
                submenu_alias, submenu_alias.id == dish_alias.submenu_id, isouter=True
            )
        )

        if dish_id:
            stmt = stmt.where(dish_alias.id == dish_id)

        result = await session.execute(stmt)
        await session.commit()
        if not dish_id:
            return result.mappings().all()
        else:
            return result.mappings().one_or_none()
