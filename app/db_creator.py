from app.database import Base, async_engine
from app.dish.model import Dish  # noqa
from app.menu.model import Menu  # noqa
from app.submenu.model import Submenu  # noqa


async def create_tables() -> None:
    """Создает по новой таблицы"""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
