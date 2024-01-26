import uuid
import sqlalchemy
from typing import Any
import pytest
from httpx import AsyncClient

from app.config import settings
from app.database import Base, async_engine

from app.main import app as fastapi_app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database():
    """Создание тестовой базы данных"""

    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def ac():
    """Асинхронный HTTP клиент"""

    async with AsyncClient(
        app=fastapi_app,
        base_url="http://test/api/v1",
    ) as ac:
        yield ac


@pytest.fixture
def menu_post() -> dict[str, str]:
    """Меню для POST запроса"""
    return {
        "title": "menu-1",
        "description": "Menu description",
    }


@pytest.fixture
def non_existen_menu_id() -> uuid.UUID:
    """Меню для POST запроса"""
    return uuid.UUID("3beeb1f1-2ec2-475e-bd38-4952f2e4235b")


@pytest.fixture
def menu_patch() -> dict[str, str]:
    """Меню для PATCH запроса"""
    return {
        "title": "New menu",
        "description": "New menu description",
    }


@pytest.fixture
def submenu_post() -> dict[str, str]:
    """Подменю для POST запроса"""
    return {
        "title": "submenu-1",
        "description": "Submenu description",
    }


@pytest.fixture
def submenu_patch() -> dict[str, str]:
    """Подменю для PATCH запроса"""
    return {
        "title": "New submenu",
        "description": "New submenu description",
    }


@pytest.fixture
def dish_post() -> dict[str, str]:
    """Блюда для POST запроса"""
    return {
        "title": "My dish",
        "description": "Dish description",
        "price": "12.67115645",
    }


@pytest.fixture
def dish_2_post() -> dict[str, str]:
    """Второе блюдо для POST запроса"""
    return {
        "title": "Second dish",
        "description": "Some another description",
        "price": "654.123",
    }


@pytest.fixture
def dish_patch() -> dict[str, str]:
    """Блюда для PATCH запроса"""
    return {
        "title": "First dish updated",
        "description": "Some description updated",
        "price": "654.123",
    }


@pytest.fixture(scope="module")
def saved_data() -> dict[str, Any]:
    """Сохраненные данные при POST запросах"""
    return {}
