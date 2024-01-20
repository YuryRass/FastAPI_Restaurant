import uuid
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.base import BaseDAO
from app.database import async_session
from app.dish.model import Dish
from app.submenu.model import Submenu

class DishDAO(BaseDAO):
    model = Dish

    @classmethod
    async def show(cls, menu_id: uuid.UUID, submenu_id: uuid.UUID, **kwargs):
        stmt = (
            select(
                Dish.id,
                Dish.title,
                Dish.description,
                Dish.price,
            )
            .select_from(Dish)
            .where(and_(Submenu.menu_id == menu_id, Dish.submenu_id == submenu_id))
            .filter_by(**kwargs)
            .join(Submenu, Submenu.id == Dish.submenu_id, isouter=True)
        )

        session: AsyncSession
        async with async_session() as session:
            result = await session.execute(stmt)
            await session.commit()
            if not kwargs:
                return result.mappings().all()
            else:
                return result.mappings().one_or_none()

    @classmethod
    async def update_dish(cls, dish_id: uuid.UUID, **data):
        updated_dish: Dish = super().update(dish_id, **data)
        dish_res = await cls.show(id=updated_dish.id)
        return dish_res