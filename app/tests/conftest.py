from typing import Any
import pytest
from httpx import AsyncClient

from app.config import settings
from app.database import Base, async_engine

from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """Заполнение тестовой базы данных"""

    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def ac():
    """Асинхронный HTTP клиент"""
    async with AsyncClient(app=fastapi_app, base_url="http://test/api/v1") as ac:
        yield ac


@pytest.fixture
def menu_post() -> dict[str, str]:
    """Меню для POST запроса"""
    return {"title": "menu-1", "description": "Menu description"}


@pytest.fixture
def menu_patch() -> dict[str, str]:
    """Меню для PATCH запроса"""
    return {"title": "New menu", "description": "New menu description"}


@pytest.fixture
def submenu_post() -> dict[str, str]:
    """Подменю для POST запроса"""
    return {"title": "submenu-1", "description": "Submenu description"}


@pytest.fixture
def submenu_patch() -> dict[str, str]:
    """Подменю для PATCH запроса"""
    return {"title": "New submenu", "description": "New submenu description"}


@pytest.fixture
def dish_post() -> dict[str, str]:
    """Блюда для POST запроса"""
    return {
        "title": "My dish",
        "description": "Dish description",
        "price": "12.905645",
    }


@pytest.fixture
def dish_2_post() -> dict[str, str]:
    """Фикстура второго блюда для POST."""
    return {
        "title": "Second dish",
        "description": "Some another description",
        "price": "654.123",
    }


@pytest.fixture
def dish_patch() -> dict[str, str]:
    """Фикстура блюда для PATCH"""
    return {
        "title": "First dish updated",
        "description": "Some description updated",
        "price": "654.123",
    }


@pytest.fixture(scope="module")
def saved_data() -> dict[str, Any]:
    """Фикстура для сохранения объектов тестирования"""
    return {}