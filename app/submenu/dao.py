import uuid

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.dao.base import BaseDAO
from app.database import async_session
from app.dish.model import Dish
from app.submenu.model import Submenu


class SubmenuDAO(BaseDAO):
    model = Submenu

    @classmethod
    async def show(
        cls,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID | None = None,
    ) -> Submenu:
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
        submenu_id: uuid.UUID | None = None,
    ) -> Submenu:
        submenu_alias = aliased(Submenu)
        dish_alias = aliased(Dish)

        # условие проверки на равенство submenu_id
        is_submenu_id = True
        if submenu_id:
            is_submenu_id = submenu_alias.id == submenu_id

        dishes_count = (
            select(func.count())
            .select_from(submenu_alias)
            .where(submenu_alias.id == dish_alias.submenu_id)
            .as_scalar()
        )

        stmt = (
            select(
                submenu_alias.id,
                submenu_alias.title,
                submenu_alias.description,
                dishes_count.label('dishes_count'),
            )
            .group_by(submenu_alias.id)
            .having(
                and_(
                    submenu_alias.menu_id == menu_id,
                    is_submenu_id,
                )
            )
        )

        result = await session.execute(stmt)
        await session.commit()
        submenu_res = result.mappings().all()
        if len(submenu_res) == 1:
            return submenu_res[0]

        return submenu_res
