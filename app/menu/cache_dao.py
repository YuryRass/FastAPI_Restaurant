from typing import Any

from app.dao.cache_base import RedisBaseDAO
from app.menu.model import Menu


class RedisMenuDAO(RedisBaseDAO):
    model = Menu

    @classmethod
    async def create_update(cls, menu: Menu, **kwargs: Any) -> None:
        await super()._create_update(menu, **kwargs)

    @classmethod
    async def delete(cls, **kwargs: Any) -> None:
        await super()._delete(**kwargs)
