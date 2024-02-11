from enum import Enum
from typing import Any
import uuid
import httpx

from app.config import settings
from app.dish.model import Dish
from app.menu.model import Menu
from app.submenu.model import Submenu
from app.utils.json_shemas import JsonMenu, JsonType


class DBModel(str, Enum):
    dish = 'dish'
    menu = 'menu'
    submenu = 'submenu'


class BaseUpdater:
    """Базовый класс для обновления моделей в БД."""

    def __init__(self, parser_data: list[JsonMenu]):
        self.parser_data = parser_data
        self.base_url = str(settings.APP_LINK)
        self.models_dict: dict[str, Any] = {
            DBModel.dish: Dish,
            DBModel.menu: Menu,
            DBModel.submenu: Submenu,
        }

    def get_models_id_from_db(self, model: str, **kwargs) -> list[uuid.UUID]:
        """Получить список всех существующих идентификаторов модели из БД."""
        url = self.base_url + self.models_dict[model].LINK.format(**kwargs)
        response = httpx.get(url).json()
        return [uuid.UUID(item['id']) for item in response]

    def add_model_data(
        self,
        model: str,
        json_data: JsonType,
        **kwargs,
    ) -> None:
        """Добавить новые данные модели в БД."""
        url = self.base_url + self.models_dict[model].LINK.format(**kwargs)
        data = {
            'id': str(json_data.id),
            'title': json_data.title,
            'description': json_data.description,
        }
        if model == 'dish':
            data['price'] = str(json_data.price)

        httpx.post(url, json=data)

    def add_models_batch(
        self, model: str, models_data: list[JsonType], **kwargs
    ) -> None:
        """Добавить новые данные моделей в БД списком."""
        for model_data in models_data:
            self.add_model_data(model, model_data, **kwargs)

    def update_model(self, model: str, model_data: JsonType, **kwargs) -> None:
        """Обновить данные модели в БД."""
        data = {'title': model_data.title, 'description': model_data.description}
        if model == DBModel.dish:
            data['price'] = str(model_data.price)
        url = self.base_url + self.models_dict[model].LONG_LINK.format(**kwargs)
        httpx.patch(url, json=data)

    def check_model(self, model: str, model_data: JsonType, **kwargs) -> None:
        """Проверка состояния модели в БД и при необходимости ее обновление."""
        url = self.base_url + self.models_dict[model].LONG_LINK.format(**kwargs)
        current_model = httpx.get(url).json()
        conditions_for_update = [
            current_model['title'] != model_data.title,
            current_model['description'] != model_data.description,
            model == DBModel.dish and current_model['price'] != str(model_data.price),
        ]

        if any(conditions_for_update):
            self.update_model(model, model_data, **kwargs)

    def delete_record_from_model(self, model: str, **kwargs) -> None:
        """Удалить запись из модели."""
        url = self.base_url + self.models_dict[model].LONG_LINK.format(**kwargs)
        httpx.delete(url)
