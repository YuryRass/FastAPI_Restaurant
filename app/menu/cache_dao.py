import pickle
from typing import Any

from app.config import settings
from app.dao.cache_base import RedisBaseDAO
from app.menu.model import Menu


class RedisMenuDAO(RedisBaseDAO):
    """CRUD операции для модели Menu в нереляц. базе данных Redis."""

    model = Menu

    @classmethod
    async def set_full_list(cls, menus: list[Menu]) -> None:
        """Запись полного списка меню в кеш."""
        await super().cacher.set(
            Menu.FULL_LINK,
            pickle.dumps(menus),
            ex=settings.EXPIRATION,
        )

    @classmethod
    async def get_full_list(cls) -> list[Menu] | None:
        """Получение полного списка меню из кеша."""
        cache = await super().cacher.get(Menu.FULL_LINK)
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    @classmethod
    async def create_update(cls, menu: Menu, **kwargs: Any) -> None:
        """Создание/обновление записи в таблице Меню."""
        await super()._create_update(menu, **kwargs)
        await cls.__delete_full_list()

    @classmethod
    async def delete(cls, **kwargs: Any) -> None:
        """Удаление записи в таблице Меню."""
        await super()._delete(**kwargs)
        await cls.__delete_full_list()

    @classmethod
    async def __delete_full_list(cls) -> None:
        """Удаление полного списка меню из кеша."""
        await super().cacher.delete(Menu.FULL_LINK)
