from typing import Any

from app.dao.cache_base import RedisBaseDAO
from app.dish.model import Dish
from app.menu.cache_dao import RedisMenuDAO
from app.submenu.cache_dao import RedisSubmenuDAO


class RedisDishDAO(RedisBaseDAO):
    """CRUD операции для модели Dish в нереляц. базе данных Redis."""
    model = Dish

    @classmethod
    async def create_update(cls, dish: Dish, **kwargs: Any) -> None:
        """Создание/обновление записи в таблице Блюдо."""
        await super()._create_update(dish, **kwargs)
        await RedisMenuDAO.delete(**kwargs)
        await RedisSubmenuDAO.delete(**kwargs)

    @classmethod
    async def delete(cls, **kwargs: Any) -> None:
        """Удаление записи в таблице Блюдо."""
        await super()._delete(**kwargs)
        await RedisMenuDAO.delete(**kwargs)
        await RedisSubmenuDAO.delete(**kwargs)
