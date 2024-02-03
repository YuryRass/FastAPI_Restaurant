import uuid

from fastapi import APIRouter, BackgroundTasks, Response

from app.menu.model import Menu
from app.menu.service import MenuService
from app.menu.shemas import OutSMenu, SMenu

router: APIRouter = APIRouter(tags=['Menus'])


@router.post(Menu.LINK)
async def add_menu(
    menu: SMenu,
    responce: Response,
    background_task: BackgroundTasks,
) -> OutSMenu:
    """
    **Добавление меню.**

    Args:
    - **menu (SMenu)**: данные о меню

    Returns:
    - **OutSMenu**: добавленные данные о меню
    """
    return await MenuService.add(menu, responce, background_task)


@router.get(Menu.LINK)
async def show_menus(background_task: BackgroundTasks) -> list[OutSMenu]:
    """
    **Получение списка всех меню.**

    Returns:
    - **list[OutSMenu]**: список всех меню
    """
    return await MenuService.show_all(background_task)


@router.get(Menu.LONG_LINK)
async def show_menu_by_id(
    menu_id: uuid.UUID, background_task: BackgroundTasks
) -> OutSMenu:
    """
    **Получние меню по его ID.**

    Args:
    - **menu_id (uuid.UUID)**: ID меню

    Returns:
    - **OutSMenu**: найденное меню
    """
    return await MenuService.show(menu_id, background_task)


@router.patch(Menu.LONG_LINK)
async def update_menu(
    menu_id: uuid.UUID,
    new_data: SMenu,
    background_task: BackgroundTasks,
) -> OutSMenu:
    """
    **Изменение данных о меню.**

    Args:
    - **menu_id (uuid.UUID)**: ID меню
    - **new_data (SMenu)**: новые данные о меню

    Returns:
    - **OutSMenu**: измененное меню
    """
    return await MenuService.update(menu_id, new_data, background_task)


@router.delete(Menu.LONG_LINK)
async def delete_menu(
    menu_id: uuid.UUID,
    background_task: BackgroundTasks,
) -> dict[str, bool | str]:
    """
    **Удаление меню.**

    Args:
    - **menu_id (uuid.UUID)**: ID меню
    """
    return await MenuService.delete(menu_id, background_task)
