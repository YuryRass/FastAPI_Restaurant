import pickle
from typing import Any, Generic, TypeVar

from aioredis import Redis

from app.database.redis import redis_cacher
from app.dish.model import Dish
from app.menu.model import Menu
from app.submenu.model import Submenu

ModelType = TypeVar('ModelType', Dish, Menu, Submenu)


class RedisBaseDAO(Generic[ModelType]):
    """Класс, описывающий основные CRUD операции для Redis."""

    model: type[ModelType]
    cacher: Redis = redis_cacher

    @classmethod
    async def delete_by_pattern(cls, pattern: str) -> None:
        """Удаление кэша по шаблону."""
        for key in await cls.cacher.keys(pattern + '*'):
            await cls.cacher.delete(key)

    @classmethod
    async def set_all(cls, items: list[ModelType], **kwargs: Any) -> None:
        """Запись всех данных модели в кеш."""
        await cls.cacher.set(
            cls.model.LINK.format(**kwargs),
            pickle.dumps(items),
            ex=3600,
        )

    @classmethod
    async def get_all(cls, **kwargs: Any) -> list[ModelType] | None:
        """Получение всех данных модели из кеша."""
        cache = await cls.cacher.get(cls.model.LINK.format(**kwargs))
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    @classmethod
    async def set(cls, item: ModelType, **kwargs: Any) -> None:
        """Запись конкрентных данных модели в кеш."""
        await cls.cacher.set(
            cls.model.LONG_LINK.format(**kwargs),
            pickle.dumps(item),
            ex=3600,
        )

    @classmethod
    async def get(cls, **kwargs: Any) -> ModelType | None:
        """Получение конкретных данных модели из кеша."""
        cache = await cls.cacher.get(cls.model.LONG_LINK.format(**kwargs))
        if cache:
            items = pickle.loads(cache)
            return items
        return None

    @classmethod
    async def delete(cls, **kwargs: Any) -> None:
        """Удаление всех связанных записей модели из кеша."""
        await cls.cacher.delete(cls.model.LINK.format(**kwargs))
        await cls.delete_by_pattern(cls.model.LONG_LINK.format(**kwargs))

    @classmethod
    async def create_update(cls, item: ModelType, **kwargs: Any) -> None:
        """Создание/изменение новой модели в кеше."""
        await cls.delete(**kwargs)

        await cls.cacher.set(
            cls.model.LONG_LINK.format(**kwargs),
            pickle.dumps(item),
            ex=3600,
        )
