from typing import Any

from app.dao.cache_base import RedisBaseDAO
from app.menu.model import Menu


class RedisMenuDAO(RedisBaseDAO):
    """CRUD операции для модели Menu в нереляц. базе данных Redis."""
    model = Menu

    @classmethod
    async def create_update(cls, menu: Menu, **kwargs: Any) -> None:
        """Создание/обновление записи в таблице Меню."""
        await super()._create_update(menu, **kwargs)

    @classmethod
    async def delete(cls, **kwargs: Any) -> None:
        """Удаление записи в таблице Меню."""
        await super()._delete(**kwargs)
