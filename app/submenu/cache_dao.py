from typing import Any

from app.dao.cache_base import RedisBaseDAO
from app.menu.cache_dao import RedisMenuDAO
from app.submenu.model import Submenu


class RedisSubmenuDAO(RedisBaseDAO):
    """CRUD операции для модели Submenu в нереляц. базе данных Redis."""
    model = Submenu

    @classmethod
    async def create_update(cls, submenu: Submenu, **kwargs: Any) -> None:
        """Создание/обновление записи в таблице Подменю."""
        await super()._create_update(submenu, **kwargs)
        await RedisMenuDAO.delete(**kwargs)

    @classmethod
    async def delete(cls, **kwargs: Any) -> None:
        """Удаление записи в таблице Подменю."""
        await super()._delete(**kwargs)
        await RedisMenuDAO.delete(**kwargs)
