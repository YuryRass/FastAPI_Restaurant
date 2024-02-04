import uuid

from fastapi import BackgroundTasks, Response, status
from sqlalchemy.exc import IntegrityError

from app.exceptions import SimilarSubmenuTitlesException, SubMenuNotFoundException
from app.menu.dao import MenuDAO
from app.submenu.cache_dao import RedisSubmenuDAO
from app.submenu.dao import SubmenuDAO
from app.submenu.shemas import OutSSubMenu, SSubMenu


class SubmenuService:
    """Сервисный слой для подменю."""
    @classmethod
    async def add(
        cls,
        menu_id: uuid.UUID,
        submenu: SSubMenu,
        responce: Response,
        background_task: BackgroundTasks,
    ) -> OutSSubMenu:
        """Добавление подменю."""
        finded_menu = await MenuDAO.show(menu_id)
        try:
            if finded_menu:
                submenu = await SubmenuDAO.add(
                    title=submenu.title,
                    description=submenu.description,
                    menu_id=menu_id,
                )
        except IntegrityError:
            raise SimilarSubmenuTitlesException
        responce.status_code = status.HTTP_201_CREATED
        added_submenu = await SubmenuDAO.show(menu_id, submenu['id'])
        background_task.add_task(
            RedisSubmenuDAO.create_update,
            added_submenu,
            menu_id=menu_id,
            submenu_id=added_submenu['id'],
        )

        return added_submenu

    @classmethod
    async def show(
        cls,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        background_task: BackgroundTasks,
    ) -> OutSSubMenu:
        """Отображение подменю."""
        res = await RedisSubmenuDAO.get(menu_id=menu_id, submenu_id=submenu_id)
        if res is not None:
            return res
        submenu = await SubmenuDAO.show(menu_id, submenu_id)
        if not submenu:
            raise SubMenuNotFoundException
        background_task.add_task(
            RedisSubmenuDAO.set,
            submenu,
            menu_id=menu_id,
            submenu_id=submenu_id,
        )

        return submenu

    @classmethod
    async def show_all(
        cls,
        menu_id: uuid.UUID,
        background_task: BackgroundTasks,
    ) -> list[OutSSubMenu] | OutSSubMenu:
        """Отображение всех подменю."""
        res = await RedisSubmenuDAO.get_all(menu_id=menu_id)
        if res is not None:
            return res
        submenus = await SubmenuDAO.show(menu_id)
        background_task.add_task(
            RedisSubmenuDAO.set_all,
            submenus,
            menu_id=menu_id,
        )

        return submenus

    @classmethod
    async def update(
        cls,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        new_data: SSubMenu,
        background_task: BackgroundTasks,
    ) -> OutSSubMenu:
        """Изменение подменю."""
        submenu = await RedisSubmenuDAO.get(menu_id=menu_id, submenu_id=submenu_id)
        if submenu is None:
            submenu = await SubmenuDAO.show(menu_id, submenu_id)
        if not submenu:
            raise SubMenuNotFoundException

        updated_submenu = await SubmenuDAO.update(
            submenu_id,
            title=new_data.title,
            description=new_data.description,
        )

        submenu_res = await SubmenuDAO.show(menu_id, updated_submenu['id'])

        background_task.add_task(
            RedisSubmenuDAO.create_update,
            submenu_res,
            menu_id=menu_id,
            submenu_id=submenu_res['id'],
        )
        return submenu_res

    @classmethod
    async def delete(
        cls,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        background_task: BackgroundTasks,
    ) -> dict[str, bool | str]:
        """Удаление подменю."""
        submenu = await SubmenuDAO.delete_record(id=submenu_id, menu_id=menu_id)
        if submenu:
            background_task.add_task(
                RedisSubmenuDAO.delete,
                menu_id=menu_id,
                submenu_id=submenu_id,
            )

            return {'status': True, 'message': 'The submenu has been deleted'}
        return {'status': False, 'message': 'Submenu not found'}
