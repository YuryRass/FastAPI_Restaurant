from typing import TypeVar

from pydantic import UUID4, BaseModel


class JsonDish(BaseModel):
    """Схема блюда."""
    id: UUID4
    title: str
    description: str
    price: float


class JsonSubmenu(BaseModel):
    """Схема подменю, включающая блюда."""
    id: UUID4
    title: str
    description: str
    dishes: list[JsonDish]


class JsonMenu(BaseModel):
    """Схема меню, включающая подменю и блюда."""
    id: UUID4
    title: str
    description: str
    submenus: list[JsonSubmenu]


JsonType = TypeVar('JsonType', JsonDish, JsonMenu, JsonSubmenu)
