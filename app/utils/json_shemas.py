import pickle
from typing import TypeVar

from pydantic import UUID4, BaseModel, model_validator

from app.database.sync_redis import redis_cacher


class JsonDish(BaseModel):
    """Схема блюда."""

    id: UUID4
    title: str
    description: str
    price: float


class UpdatedJsonDish(JsonDish):
    """Схема блюда с измененной ценой (с учетом скидки)."""

    @model_validator(mode='after')
    def validate_atts(self):
        res = redis_cacher.get(str(self.id))
        if res:
            self.price = float(pickle.loads(res))
        self.price = round(self.price, 2)
        return self


class JsonSubmenu(BaseModel):
    """Схема подменю, включающая блюда."""

    id: UUID4
    title: str
    description: str
    dishes: list[JsonDish]


class JsonSubmenuOut(BaseModel):
    """Схема подменю, включающая блюда (для вывода в API)."""

    id: UUID4
    title: str
    description: str
    dishes: list[UpdatedJsonDish]


class JsonMenu(BaseModel):
    """Схема меню, включающая подменю и блюда."""

    id: UUID4
    title: str
    description: str
    submenus: list[JsonSubmenu]


class JsonMenuOut(BaseModel):
    """Схема меню, включающая подменю и блюда (для вывода в API)."""

    id: UUID4
    title: str
    description: str
    submenus: list[JsonSubmenuOut]


JsonType = TypeVar('JsonType', JsonDish, JsonMenu, JsonSubmenu)
