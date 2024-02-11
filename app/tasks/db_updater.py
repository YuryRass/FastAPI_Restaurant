import uuid

from app.utils.base_updater import BaseUpdater, DBModel
from app.utils.json_shemas import JsonDish, JsonSubmenu


class DBUpdater(BaseUpdater):
    """Обновление данных в БД после чтения excel файла."""

    def run(self) -> None:
        """Запуск обновления данных в БД."""
        self.check_menus()

    def check_menus(self) -> None:
        """Проверка меню в БД и их обновление в соответствии с файлом."""
        menus_id = super().get_models_id_from_db(DBModel.menu)
        for menu in self.parser_data:
            if menu.id not in menus_id:
                super().add_model_data(DBModel.menu, menu)
                super().add_models_batch(
                    DBModel.submenu,
                    menu.submenus,
                    menu_id=menu.id,
                )
                for submenu in menu.submenus:
                    super().add_models_batch(
                        DBModel.dish,
                        submenu.dishes,
                        submenu_id=submenu.id,
                        menu_id=menu.id,
                    )
            else:
                super().check_model(DBModel.menu, menu, menu_id=menu.id)
                if menu.submenus:
                    self.__check_submenus(
                        submenus=menu.submenus,
                        menu_id=menu.id,
                    )
                menus_id.remove(menu.id)
        for id_ in menus_id:
            super().delete_record_from_model(DBModel.menu, menu_id=id_)

    def __check_dishes(
        self,
        dishes: list[JsonDish],
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
    ) -> None:
        """Проверка блюд в БД и их обновление в соответствии с файлом."""
        dishes_id = super().get_models_id_from_db(
            DBModel.dish,
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        for dish in dishes:
            if dish.id not in dishes_id:
                super().add_model_data(
                    DBModel.dish,
                    dish,
                    submenu_id=submenu_id,
                    menu_id=menu_id,
                )
            else:
                super().check_model(
                    DBModel.dish,
                    dish,
                    menu_id=menu_id,
                    submenu_id=submenu_id,
                    dish_id=dish.id,
                )
                dishes_id.remove(dish.id)
        for id_ in dishes_id:
            super().delete_record_from_model(
                DBModel.dish,
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish_id=id_,
            )

    def __check_submenus(
        self,
        submenus: list[JsonSubmenu],
        menu_id: uuid.UUID,
    ) -> None:
        """Проверка подменю в БД и их обновление в соответствии с файлом."""
        submenus_id = self.get_models_id_from_db(DBModel.submenu, menu_id=menu_id)
        for submenu in submenus:
            if submenu.id not in submenus_id:
                super().add_model_data(DBModel.submenu, submenu, menu_id=menu_id)
                super().add_models_batch(
                    DBModel.dish,
                    submenu.dishes,
                    submenu_id=submenu.id,
                    menu_id=menu_id,
                )
            else:
                super().check_model(
                    DBModel.submenu,
                    submenu,
                    menu_id=menu_id,
                    submenu_id=submenu.id,
                )
                if submenu.dishes:
                    self.__check_dishes(
                        dishes=submenu.dishes,
                        menu_id=menu_id,
                        submenu_id=submenu.id,
                    )
                submenus_id.remove(submenu.id)
        for id_ in submenus_id:
            super().delete_record_from_model(
                DBModel.submenu, menu_id=menu_id, submenu_id=id_
            )
