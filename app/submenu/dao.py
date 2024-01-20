import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import async_session
from app.dish.model import Dish
from app.dao.base import BaseDAO
from app.submenu.model import Submenu


class SubmenuDAO(BaseDAO):
    model = Submenu

    @classmethod
    async def show(cls, **kwargs):
        stmt = (
            select(
                Submenu.id,
                Submenu.title,
                Submenu.description,
                func.count(Dish.submenu_id)
                .filter(Dish.submenu_id.is_not(None))
                .label("dishes_count"),
            )
            .select_from(Submenu)
            .filter_by(**kwargs)
            .join(Dish, Submenu.id == Dish.submenu_id, isouter=True)
            .group_by(Submenu, Dish.submenu_id)
        )

        session: AsyncSession
        async with async_session() as session:
            result = await session.execute(stmt)
            await session.commit()
            submenu_res = result.mappings().all()
            if len(submenu_res) == 1:
                return submenu_res[0]
            return submenu_res

    @classmethod
    async def update_submenu(cls, submenu_id: uuid.UUID, **data):
        updated_submenu: Submenu = super().update(submenu_id, **data)
        submenu_res = await cls.show(id=updated_submenu.id)
        return submenu_res
