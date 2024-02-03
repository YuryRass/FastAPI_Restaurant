import uuid

from fastapi import BackgroundTasks, Response, status
from sqlalchemy.exc import IntegrityError

from app.exceptions import MenuNotFoundException, SimilarMenuTitlesException
from app.menu.cache_dao import RedisMenuDAO
from app.menu.dao import MenuDAO
from app.menu.shemas import OutSMenu, SMenu


class MenuService:
    @classmethod
    async def add(
        cls,
        menu: SMenu,
        responce: Response,
        background_task: BackgroundTasks,
    ) -> OutSMenu:
        try:
            menu_res = await MenuDAO.add(
                title=menu.title,
                description=menu.description,
            )
        except IntegrityError:
            raise SimilarMenuTitlesException

        responce.status_code = status.HTTP_201_CREATED
        added_menu = await MenuDAO.show(menu_res['id'])
        background_task.add_task(
            RedisMenuDAO.create_update,
            added_menu,
            menu_id=added_menu.id,
        )
        return added_menu

    @classmethod
    async def show_all(cls, background_task: BackgroundTasks) -> list[OutSMenu]:
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
        menu = await RedisMenuDAO.get(menu_id=menu_id)
        if menu is None:
            menu = await MenuDAO.show(menu_id)
        if not menu:
            raise MenuNotFoundException

        updated_menu = await MenuDAO.update(
            menu_id,
            title=new_data.title,
            description=new_data.description,
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
        menu = await MenuDAO.delete_record(id=menu_id)
        if menu:
            background_task.add_task(RedisMenuDAO.delete, menu_id=menu_id)
            return {'status': True, 'message': 'The menu has been deleted'}
        return {'status': False, 'message': 'Menu not found'}
