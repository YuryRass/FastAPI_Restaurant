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
        menus_id_from_db = await super().get_models_id_from_db(DBModel.menu)
        remote_menus_id = []
        for menu in self.parser_data:
            remote_menus_id.append(menu.id)
            if menu.id not in menus_id_from_db:
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
                menus_id_from_db.remove(menu.id)
                await super().check_model(DBModel.menu, menu)
                if menu.submenus:
                    await self.__check_submenus(
                        menu.submenus,
                        menu.id,
                    )
        menus_id_for_delete = [x for x in menus_id_from_db if x not in remote_menus_id]
        for id_ in menus_id_for_delete:
            await super().delete_record_from_model(DBModel.menu, id=id_)

    async def __check_submenus(
        self,
        submenus: list[JsonSubmenu],
        menu_id: uuid.UUID,
    ) -> None:
        """Проверка подменю в БД и их обновление в соответствии с файлом."""
        submenus_id_from_db = await super().get_models_id_from_db(DBModel.submenu, menu_id=menu_id)
        remote_submenus_id = [submenu.id for submenu in submenus]
        submenus_id_for_delete = [x for x in submenus_id_from_db if x not in remote_submenus_id]
        for submenu in submenus:
            if submenu.id not in submenus_id_from_db:
                await super().add_model_data(DBModel.submenu, submenu, menu_id)
                await super().add_models_batch(DBModel.dish, submenu.dishes, submenu.id)
            else:
                await super().check_model(DBModel.submenu, submenu)
                if submenu.dishes:
                    self.dishes_id = [item.id for item in submenu.dishes]
                    await self.__check_dishes(
                        submenu.dishes,
                        submenu.id,
                    )
        for id_ in submenus_id_for_delete:
            await super().delete_record_from_model(DBModel.submenu, id=id_)

    async def __check_dishes(
        self,
        dishes: list[JsonDish],
        submenu_id: uuid.UUID,
    ) -> None:
        """Проверка блюд в БД и их обновление в соответствии с файлом."""
        dishes_id_from_db = await super().get_models_id_from_db(DBModel.dish, submenu_id=submenu_id)
        remote_dishes_id = [dish.id for dish in dishes]
        dishes_id_for_delete = [x for x in dishes_id_from_db if x not in remote_dishes_id]
        for dish in dishes:
            if dish.id not in dishes_id_from_db:
                await super().add_model_data(DBModel.dish, dish, submenu_id)
            else:
                await super().check_model(DBModel.dish, dish)
        for id_ in dishes_id_for_delete:
            await super().delete_record_from_model(DBModel.dish, id=id_)
