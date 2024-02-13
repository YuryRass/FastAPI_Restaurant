import uuid
from enum import Enum
from typing import Any, Generic, TypeVar

from app.config import settings
from app.dish.dao import DishDAO
from app.menu.dao import MenuDAO
from app.submenu.dao import SubmenuDAO
from app.utils.json_shemas import JsonMenu, JsonType


class DBModel(str, Enum):
    dish = 'dish'
    menu = 'menu'
    submenu = 'submenu'


TypeDAO = TypeVar('TypeDAO', DishDAO, MenuDAO, SubmenuDAO)


class BaseUpdater(Generic[TypeDAO]):
    """Базовый класс для обновления моделей в БД."""

    def __init__(self, parser_data: list[JsonMenu]):
        self.parser_data = parser_data
        self.base_url = str(settings.APP_LINK)
        self.model_dao: dict[str, TypeDAO] = {
            DBModel.dish: self.__get_dao(DBModel.dish),
            DBModel.menu: self.__get_dao(DBModel.menu),
            DBModel.submenu: self.__get_dao(DBModel.submenu),
        }

    def __get_dao(self, model: str) -> Any:
        if model == DBModel.dish:
            return DishDAO
        elif model == DBModel.submenu:
            return SubmenuDAO
        else:
            return MenuDAO

    async def get_models_id_from_db(self, model: str) -> list[uuid.UUID]:
        """Получить список всех существующих идентификаторов модели из БД."""
        model_identifiers = await self.model_dao[model].get_identifiers()
        return model_identifiers

    async def add_model_data(
        self,
        model: str,
        json_data: JsonType,
        dependent_model_id: uuid.UUID | None = None,
    ) -> None:
        """Добавить новые данные модели в БД."""
        data = {
            'id': json_data.id,
            'title': json_data.title,
            'description': json_data.description,
        }
        if model == DBModel.dish and dependent_model_id is not None:
            data['price'] = json_data.price
            data['submenu_id'] = dependent_model_id
        elif model == DBModel.submenu and dependent_model_id is not None:
            data['menu_id'] = dependent_model_id
        await self.model_dao[model].add(**data)

    async def add_models_batch(
        self,
        model: str,
        models_data: list[JsonType],
        dependent_id: uuid.UUID | None = None,
    ) -> None:
        """Добавить новые данные моделей в БД списком."""
        for model_data in models_data:
            await self.add_model_data(model, model_data, dependent_id)

    async def update_model(self, model: str, model_data: JsonType) -> None:
        """Обновить данные модели в БД."""
        data: dict[str, str | float] = {'title': model_data.title, 'description': model_data.description}
        if model == DBModel.dish:
            data['price'] = model_data.price
        await self.model_dao[model].update(model_data.id, **data)

    async def check_model(self, model: str, model_data: JsonType) -> None:
        """Проверка состояния модели в БД и при необходимости ее обновление."""
        current_model = await self.model_dao[model].get_by_id(model_data.id)
        assert current_model is not None
        conditions_for_update = [
            current_model['title'] != model_data.title,
            current_model['description'] != model_data.description,
            model == DBModel.dish and current_model['price'] != model_data.price,
        ]

        if any(conditions_for_update):
            await self.update_model(model, model_data)

    async def delete_record_from_model(self, model: str, **kwargs) -> None:
        """Удалить запись из модели."""
        await self.model_dao[model].delete_record(**kwargs)
