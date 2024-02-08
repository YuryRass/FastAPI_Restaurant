import uuid

from fastapi import BackgroundTasks, Response, status
from sqlalchemy.exc import IntegrityError

from app.exceptions import MenuNotFoundException, SimilarMenuTitlesException
from app.menu.cache_dao import RedisMenuDAO
from app.menu.dao import MenuDAO
from app.menu.shemas import OutSMenu, SMenu
from app.tasks.schemas import JsonMenu


class MenuService:
    """Сервисный слой для меню."""

    @classmethod
    async def show_full_list(cls, background_task: BackgroundTasks) -> list[JsonMenu]:
        """
        Отображение всех меню со всеми связанными подменю
        и со всеми связанными блюдами.
        """
        res = await RedisMenuDAO.get_full_list()
        if res is not None:
            return res
        menus = await MenuDAO.show_full_list()
        background_task.add_task(RedisMenuDAO.set_full_list, menus)
        return menus

    @classmethod
    async def add(
        cls,
        menu: SMenu,
        response: Response,
        background_task: BackgroundTasks,
    ) -> OutSMenu:
        """Добавление меню."""
        try:
            menu_res = await MenuDAO.add(**menu.model_dump(exclude_none=True))
        except IntegrityError:
            raise SimilarMenuTitlesException

        response.status_code = status.HTTP_201_CREATED
        added_menu = await MenuDAO.show(menu_res['id'])
        background_task.add_task(
            RedisMenuDAO.create_update,
            added_menu,
            menu_id=added_menu['id'],
        )
        return added_menu

    @classmethod
    async def show_all(cls, background_task: BackgroundTasks) -> list[OutSMenu]:
        """Отображение списка всех меню."""
        res = await RedisMenuDAO.get_all()
        if res is not None:
            return res
        menus = await MenuDAO.show_all()
        background_task.add_task(RedisMenuDAO.set_all, menus)

        return menus

    @classmethod
    async def show(
        cls,
        menu_id: uuid.UUID,
        background_task: BackgroundTasks,
    ) -> OutSMenu:
        """Отображение меню."""
        res = await RedisMenuDAO.get(menu_id=menu_id)
        if res is not None:
            return res
        menu = await MenuDAO.show(menu_id)
        if not menu:
            raise MenuNotFoundException
        background_task.add_task(RedisMenuDAO.set, menu, menu_id=menu_id)

        return menu

    @classmethod
    async def update(
        cls,
        menu_id: uuid.UUID,
        new_data: SMenu,
        background_task: BackgroundTasks,
    ) -> OutSMenu:
        """Изменение меню."""
        menu = await RedisMenuDAO.get(menu_id=menu_id)
        if menu is None:
            menu = await MenuDAO.show(menu_id)
        if not menu:
            raise MenuNotFoundException
        updated_menu = await MenuDAO.update(
            menu_id, **new_data.model_dump(exclude_none=True)
        )

        menu_res = await MenuDAO.show(updated_menu['id'])
        background_task.add_task(
            RedisMenuDAO.create_update,
            menu_res,
            menu_id=menu_id,
        )
        return menu_res

    @classmethod
    async def delete(
        cls,
        menu_id: uuid.UUID,
        background_task: BackgroundTasks,
    ) -> dict[str, bool | str]:
        """Удаление меню."""
        menu = await MenuDAO.delete_record(id=menu_id)
        if menu:
            background_task.add_task(RedisMenuDAO.delete, menu_id=menu_id)
            return {'status': True, 'message': 'The menu has been deleted'}
        return {'status': False, 'message': 'Menu not found'}
