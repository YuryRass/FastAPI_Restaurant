import uuid
from enum import Enum
from typing import Any

import httpx

from app.config import settings
from app.dish.model import Dish
from app.menu.model import Menu
from app.submenu.model import Submenu
from app.utils.json_shemas import JsonDish, JsonMenu, JsonSubmenu, JsonType


class DBModel(str, Enum):
    dish = 'dish'
    menu = 'menu'
    submenu = 'submenu'


class DBUpdater:
    """Обновление данных в БД после чтения excel файла."""

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

    def check_dishes(
        self,
        dishes: list[JsonDish],
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> None:
        """Проверить состояние блюд в базе и привести
        в соответствие с файлом."""
        dishes_id = self.get_models_id_from_db(
            DBModel.dish,
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        for dish in dishes:
            if dish.id not in dishes_id:
                self.add_model_data(
                    DBModel.dish,
                    dish,
                    submenu_id=submenu_id,
                    menu_id=menu_id,
                )
            else:
                self.check_model(
                    DBModel.dish,
                    dish,
                    menu_id=menu_id,
                    submenu_id=submenu_id,
                    dish_id=dish.id,
                )
                dishes_id.remove(dish.id)
        for id_ in dishes_id:
            self.delete_record_from_model(
                DBModel.dish,
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish_id=id_,
            )

    def check_submenus(
        self,
        submenus: list[JsonSubmenu],
        menu_id: uuid.UUID,
    ) -> None:
        """Проверить состояние подменю в базе и привести
        в соответствие с файлом."""
        submenus_id = self.get_models_id_from_db(DBModel.submenu, menu_id=menu_id)
        for submenu in submenus:
            if submenu.id not in submenus_id:
                self.add_model_data(DBModel.submenu, submenu, menu_id=menu_id)
                self.add_models_batch(
                    DBModel.dish,
                    submenu.dishes,
                    submenu_id=submenu.id,
                    menu_id=menu_id,
                )
            else:
                self.check_model(
                    DBModel.submenu,
                    submenu,
                    menu_id=menu_id,
                    submenu_id=submenu.id,
                )
                if submenu.dishes:
                    self.check_dishes(
                        dishes=submenu.dishes,
                        menu_id=menu_id,
                        submenu_id=submenu.id,
                    )
                submenus_id.remove(submenu.id)
        for id_ in submenus_id:
            self.delete_record_from_model(
                DBModel.submenu, menu_id=menu_id, submenu_id=id_
            )

    def check_menus(self) -> None:
        """Проверить состояние меню в базе и привести
        в соответствие с файлом."""
        menus_id = self.get_models_id_from_db('menu')
        for menu in self.parser_data:
            if menu.id not in menus_id:
                self.add_model_data(DBModel.menu, menu)
                self.add_models_batch(
                    DBModel.submenu,
                    menu.submenus,
                    menu_id=menu.id,
                )
                for submenu in menu.submenus:
                    self.add_models_batch(
                        DBModel.dish,
                        submenu.dishes,
                        submenu_id=submenu.id,
                        menu_id=menu.id,
                    )
            else:
                self.check_model(DBModel.menu, menu, menu_id=menu.id)
                if menu.submenus:
                    self.check_submenus(
                        submenus=menu.submenus,
                        menu_id=menu.id,
                    )
                menus_id.remove(menu.id)
        for id_ in menus_id:
            self.delete_record_from_model(DBModel.menu, menu_id=id_)

    def run(self) -> None:
        """Запустить обновление данных в БД."""
        self.check_menus()
