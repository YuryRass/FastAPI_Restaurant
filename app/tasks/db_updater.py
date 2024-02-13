import uuid

from app.utils.base_updater import BaseUpdater, DBModel
from app.utils.json_shemas import JsonDish, JsonSubmenu


class DBUpdater(BaseUpdater):
    """Обновление данных в БД после чтения excel файла."""

    async def run(self) -> None:
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
                        submenus=menu.submenus,
                        menu_id=menu.id,
                    )
        for id_ in menus_id:
            await super().delete_record_from_model(DBModel.menu, id=id_)

    async def __check_submenus(
        self,
        submenus: list[JsonSubmenu],
        menu_id: uuid.UUID,
    ) -> None:
        """Проверка подменю в БД и их обновление в соответствии с файлом."""
        submenus_id = await self.get_models_id_from_db(DBModel.submenu)
        for submenu in submenus:
            if submenu.id not in submenus_id:
                await super().add_model_data(DBModel.submenu, submenu, menu_id)
                await super().add_models_batch(DBModel.dish, submenu.dishes, submenu.id)
            else:
                submenus_id.remove(submenu.id)
                await super().check_model(DBModel.submenu, submenu)
                if submenu.dishes:
                    await self.__check_dishes(
                        submenu.dishes,
                        submenu.id,
                    )
        print(f'*******************submenus id: {submenus_id}')
        for id_ in submenus_id:
            await super().delete_record_from_model(DBModel.submenu, id=id_)

    async def __check_dishes(
        self,
        dishes: list[JsonDish],
        submenu_id: uuid.UUID,
    ) -> None:
        """Проверка блюд в БД и их обновление в соответствии с файлом."""
        dishes_id = await super().get_models_id_from_db(DBModel.dish)
        for dish in dishes:
            if dish.id not in dishes_id:
                await super().add_model_data(DBModel.dish, dish, submenu_id)
            else:
                dishes_id.remove(dish.id)  # TODO create task or убрать операцию удаления, сделать пересечение списков
                # TODO посмотри asyncio-celery
                # TODO как запустить shedule в отдельном процессе?
                await super().check_model(DBModel.dish, dish)
        for id_ in dishes_id:
            await super().delete_record_from_model(DBModel.dish, id=id_)
