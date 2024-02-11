import uuid
from typing import Any

import httpx

from app.config import settings
from app.dish.model import Dish
from app.menu.model import Menu
from app.submenu.model import Submenu
from app.utils.json_shemas import JsonDish, JsonMenu, JsonSubmenu, JsonType


class DBUpdater:
    """Обновление данных в БД после чтения excel файла."""

    def __init__(self, parser_data: list[JsonMenu]):
        self.parser_data = parser_data
        self.base_url = settings.APP_LINK
        self.models_dict: dict[str, Any] = {
            'dish': Dish,
            'menu': Menu,
            'submenu': Submenu,
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

    # def post_menu(self, menu: JsonMenu) -> None:
    #     """Запостить новое меню в базу."""
    #     url = self.base_url + Menu.LINK
    #     data = {
    #         "id": str(menu.id),
    #         "title": menu.title,
    #         "description": menu.description,
    #     }
    #     httpx.post(url, json=data)

    # def post_submenu(
    #     self,
    #     submenu: JsonSubmenu,
    #     menu_id: uuid.UUID,
    # ) -> None:
    #     """Запостить новое подменю в базу."""
    #     url = self.base_url + Submenu.LINK.format(menu_id=menu_id)
    #     data = {
    #         "id": str(submenu.id),
    #         "title": submenu.title,
    #         "description": submenu.description,
    #     }
    #     httpx.post(url, json=data)

    # def post_dish(
    #     self,
    #     dish: JsonDish,
    #     submenu_id: uuid.UUID,
    #     menu_id: uuid.UUID,
    # ) -> None:
    #     """Запостить новое блюдо в базу."""
    #     url = self.base_url + Dish.LINK.format(
    #         menu_id=menu_id,
    #         submenu_id=submenu_id,
    #     )
    #     data = {
    #         "id": str(dish.id),
    #         "title": dish.title,
    #         "description": dish.description,
    #         "price": str(dish.price),
    #     }
    # httpx.post(url, json=data)

    def add_models_batch(
        self, model: str, models_data: list[JsonType], **kwargs
    ) -> None:
        """Добавить новые данные моделей в БД списком."""
        for model_data in models_data:
            self.add_model_data(model, model_data, **kwargs)

    # def post_submenus_batch(
    #     self, submenus: list[JsonSubmenu], menu_id: uuid.UUID
    # ) -> None:
    #     """Запостить новые подменю в базу списком."""
    #     for submenu in submenus:
    #         self.post_submenu(
    #             submenu=submenu,
    #             menu_id=menu_id,
    #         )

    # def post_dishes_batch(
    #     self,
    #     dishes: list[JsonDish],
    #     submenu_id: uuid.UUID,
    #     menu_id: uuid.UUID,
    # ) -> None:
    #     """Запостить новые блюда в базу списком."""
    #     for dish in dishes:
    #         self.post_dish(
    #             dish=dish,
    #             submenu_id=submenu_id,
    #             menu_id=menu_id,
    #         )

    def patch_menu(self, menu: JsonMenu) -> None:
        """Обновить данные о меню в базе."""
        data = {
            'title': menu.title,
            'description': menu.description,
        }
        url = self.base_url + Menu.LONG_LINK.format(menu_id=menu.id)
        httpx.patch(url, json=data)

    def check_menu(self, menu: JsonMenu) -> None:
        """Проверить состояние меню в базе и по необходимости обновить."""
        url = self.base_url + Menu.LONG_LINK.format(menu_id=menu.id)
        current_menu = httpx.get(url).json()
        if (
            current_menu['title'] != menu.title or current_menu['description'] != menu.description
        ):
            self.patch_menu(menu=menu)

    def patch_submenu(
        self,
        submenu: JsonSubmenu,
        menu_id: uuid.UUID,
    ) -> None:
        """Обновить данные о подменю в базе."""
        data = {
            'title': submenu.title,
            'description': submenu.description,
        }
        url = self.base_url + Submenu.LONG_LINK.format(
            menu_id=menu_id,
            submenu_id=str(submenu.id),
        )
        httpx.patch(url, json=data)

    def check_submenu(
        self,
        submenu: JsonSubmenu,
        menu_id: uuid.UUID,
    ) -> None:
        """Проверить состояние подменю в базе и по необходимости обновить."""
        url = self.base_url + Submenu.LONG_LINK.format(
            menu_id=menu_id,
            submenu_id=str(submenu.id),
        )
        current_submenu = httpx.get(url).json()
        if (
            current_submenu['title'] != submenu.title or current_submenu['description'] != submenu.description
        ):
            self.patch_submenu(submenu=submenu, menu_id=menu_id)

    def patch_dish(
        self,
        dish: JsonDish,
        submenu_id: uuid.UUID,
        menu_id: uuid.UUID,
    ) -> None:
        """Обновить данные о блюде в базе."""
        data = {
            'title': dish.title,
            'description': dish.description,
            'price': str(dish.price),
        }
        url = self.base_url + Dish.LONG_LINK.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish.id,
        )
        httpx.patch(url, json=data)

    def check_dish(
        self,
        dish: JsonDish,
        submenu_id: uuid.UUID,
        menu_id: uuid.UUID,
    ) -> None:
        """Проверить состояние блюда в базе и по необходимости обновить."""
        url = self.base_url + Dish.LONG_LINK.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish.id,
        )
        current_dish = httpx.get(url).json()

        if (
            current_dish['title'] != dish.title or current_dish['description'] != dish.description or current_dish['price'] != str(
                dish.price)
        ):
            self.patch_dish(
                dish=dish,
                submenu_id=submenu_id,
                menu_id=menu_id,
            )

    def delete_menu(self, menu_id: uuid.UUID) -> None:
        """Удалить меню из базы."""
        url = self.base_url + Menu.LONG_LINK.format(menu_id=menu_id)
        httpx.delete(url)

    def delete_submenu(self, submenu_id: uuid.UUID, menu_id: uuid.UUID) -> None:
        """Удалить подменю из базы."""
        url = self.base_url + Submenu.LONG_LINK.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        httpx.delete(url)

    def delete_dish(
        self, dish_id: uuid.UUID, menu_id: uuid.UUID, submenu_id: uuid.UUID
    ) -> None:
        """Удалить блюдо из базы."""
        url = self.base_url + Dish.LONG_LINK.format(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )
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
            'dish',
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        for dish in dishes:
            if dish.id not in dishes_id:
                self.add_model_data(
                    'dish',
                    dish,
                    submenu_id=submenu_id,
                    menu_id=menu_id,
                )
            else:
                self.check_dish(dish, submenu_id, menu_id)
                dishes_id.remove(dish.id)
        for id in dishes_id:
            self.delete_dish(
                dish_id=id,
                menu_id=menu_id,
                submenu_id=submenu_id,
            )

    def check_submenus(
        self,
        submenus: list[JsonSubmenu],
        menu_id: uuid.UUID,
    ) -> None:
        """Проверить состояние подменю в базе и привести
        в соответствие с файлом."""
        submenus_id = self.get_models_id_from_db('submenu', menu_id=menu_id)
        for submenu in submenus:
            if submenu.id not in submenus_id:
                self.add_model_data('submenu', submenu, menu_id=menu_id)
                self.add_models_batch(
                    'dish',
                    submenu.dishes,
                    submenu_id=submenu.id,
                    menu_id=menu_id,
                )
            else:
                self.check_submenu(
                    submenu=submenu,
                    menu_id=menu_id,
                )
                if submenu.dishes:
                    self.check_dishes(
                        dishes=submenu.dishes,
                        menu_id=menu_id,
                        submenu_id=submenu.id,
                    )
                submenus_id.remove(submenu.id)
        for id in submenus_id:
            self.delete_submenu(
                submenu_id=id,
                menu_id=menu_id,
            )

    def check_menus(self) -> None:
        """Проверить состояние меню в базе и привести
        в соответствие с файлом."""
        menus_id = self.get_models_id_from_db('menu')
        for menu in self.parser_data:
            if menu.id not in menus_id:
                self.add_model_data('menu', menu)
                self.add_models_batch(
                    'submenu',
                    menu.submenus,
                    menu_id=menu.id,
                )
                for submenu in menu.submenus:
                    self.add_models_batch(
                        'dish',
                        submenu.dishes,
                        submenu_id=submenu.id,
                        menu_id=menu.id,
                    )
            else:
                self.check_menu(menu=menu)
                if menu.submenus:
                    self.check_submenus(
                        submenus=menu.submenus,
                        menu_id=menu.id,
                    )
                menus_id.remove(menu.id)
        for i in menus_id:
            self.delete_menu(menu_id=i)

    def run(self) -> None:
        """Запустить обновление данных в базе."""
        self.check_menus()
