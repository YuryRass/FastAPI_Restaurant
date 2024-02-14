import uuid

from app.utils.base_updater import BaseUpdater, DBModel
from app.utils.json_shemas import JsonDish, JsonMenu, JsonSubmenu


class DBUpdater(BaseUpdater):
    """Обновление данных в БД после чтения excel файла."""

    def __init__(self, parser_data: list[JsonMenu]):
        super().__init__(parser_data)

    async def run_update_db(self) -> None:
        """Запуск обновления данных в БД."""
        await self.check_menus()

    async def check_menus(self) -> None:
        """Проверка меню в БД и их обновление в соответствии с файлом."""
        menus_id = await super().get_models_id_from_db(DBModel.menu)
        for menu in self.parser_data:
            if menu.id not in menus_id:
                await super().add_model_data(DBModel.menu, menu)
                await super().add_models_batch(
                    DBModel.submenu,
                    menu.submenus,
                    menu.id,
                )
                for submenu in menu.submenus:
                    await super().add_models_batch(
                        DBModel.dish,
                        submenu.dishes,
                        submenu.id,
                    )
            else:
                menus_id.remove(menu.id)
                await super().check_model(DBModel.menu, menu)
                if menu.submenus:
                    await self.__check_submenus(
                        menu.submenus,
                        menu.id,
                    )
        for id_ in menus_id:
            await super().delete_record_from_model(DBModel.menu, id=id_)

    async def __check_submenus(
        self,
        submenus: list[JsonSubmenu],
        menu_id: uuid.UUID,
    ) -> None:
        """Проверка подменю в БД и их обновление в соответствии с файлом."""
        submenus_id_from_db = await super().get_models_id_from_db(DBModel.submenu)
        current_submenus_id = [submenu.id for submenu in submenus]
        for submenu in submenus:
            if submenu.id not in submenus_id_from_db:
                await super().add_model_data(DBModel.submenu, submenu, menu_id)
                await super().add_models_batch(DBModel.dish, submenu.dishes, submenu.id)
            else:
                current_submenus_id.remove(submenu.id)
                await super().check_model(DBModel.submenu, submenu)
                if submenu.dishes:
                    self.dishes_id = [item.id for item in submenu.dishes]
                    await self.__check_dishes(
                        submenu.dishes,
                        submenu.id,
                    )
        for id_ in current_submenus_id:
            await super().delete_record_from_model(DBModel.submenu, id=id_)

    async def __check_dishes(
        self,
        dishes: list[JsonDish],
        submenu_id: uuid.UUID,
    ) -> None:
        """Проверка блюд в БД и их обновление в соответствии с файлом."""
        dishes_id_from_db = await super().get_models_id_from_db(DBModel.dish)
        current_dishes_id = [dish.id for dish in dishes]
        for dish in dishes:
            if dish.id not in dishes_id_from_db:
                await super().add_model_data(DBModel.dish, dish, submenu_id)
            else:
                current_dishes_id.remove(dish.id)
                await super().check_model(DBModel.dish, dish)
        for id_ in current_dishes_id:
            await super().delete_record_from_model(DBModel.dish, id=id_)
