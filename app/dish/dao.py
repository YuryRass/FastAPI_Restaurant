import uuid

from sqlalchemy import Select, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from app.dao.base import BaseDAO
from app.database.database import async_session
from app.dish.model import Dish
from app.submenu.model import Submenu


class DishDAO(BaseDAO):
    """CRUD операции для блюда."""

    model = Dish
    dish_alias = aliased(Dish)
    submenu_alias = aliased(Submenu)

    @classmethod
    async def show(
        cls,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
    ) -> Dish:
        """Отображение блюда."""
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
    async def show_all(
        cls,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> list[Dish]:
        """Отображение списка блюд."""
        session: AsyncSession
        async with async_session() as session:
            res = await cls.__get_dishes_info(
                session,
                menu_id,
                submenu_id,
            )
            return res

    @classmethod
    async def __get_dish_info(
        cls,
        session: AsyncSession,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
    ) -> Dish:
        """Составление и исполнение запроса о выводе блюда."""
        stmt = (
            cls.__get_dishes_info_query(menu_id, submenu_id)
            .where(cls.dish_alias.id == dish_id)
        )
        result = await session.execute(stmt)
        res = result.mappings().all()
        if res:
            return res[0]
        return res

    @classmethod
    async def __get_dishes_info(
        cls,
        session: AsyncSession,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> list[Dish]:
        stmt = cls.__get_dishes_info_query(menu_id, submenu_id)

        result = await session.execute(stmt)
        return result.mappings().all()

    @classmethod
    def __get_dishes_info_query(
        cls,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> Select[tuple[uuid.UUID, str, str | None, float]]:
        """Получение запроса о выводе блюд."""
        return (
            select(
                cls.dish_alias.id,
                cls.dish_alias.title,
                cls.dish_alias.description,
                cls.dish_alias.price,
            )
            .select_from(cls.dish_alias)
            .where(
                and_(
                    cls.submenu_alias.menu_id == menu_id,
                    cls.dish_alias.submenu_id == submenu_id,
                )
            )
            .join(
                cls.submenu_alias,
                cls.submenu_alias.id == cls.dish_alias.submenu_id,
                isouter=True,
            )
        )
