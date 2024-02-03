import uuid

from fastapi import APIRouter, BackgroundTasks, Response

from app.submenu.model import Submenu
from app.submenu.service import SubmenuService
from app.submenu.shemas import OutSSubMenu, SSubMenu

router: APIRouter = APIRouter(tags=['Submenus'])


@router.post(Submenu.LINK)
async def add_submenu(
    menu_id: uuid.UUID,
    menu: SSubMenu,
    responce: Response,
    backgraiund_task: BackgroundTasks,
) -> OutSSubMenu:
    return await SubmenuService.add(menu_id, menu, responce, backgraiund_task)


@router.get(Submenu.LONG_LINK)
async def show_submenu_by_id(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    background_task: BackgroundTasks,
) -> OutSSubMenu:
    return await SubmenuService.show(menu_id, submenu_id, background_task)


@router.get(Submenu.LINK)
async def show_submenus(
    menu_id: uuid.UUID,
    background_task: BackgroundTasks,
) -> list[OutSSubMenu] | OutSSubMenu:
    return await SubmenuService.show_all(menu_id, background_task)


@router.patch(Submenu.LONG_LINK)
async def update_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    new_data: SSubMenu,
    background_task: BackgroundTasks,
) -> OutSSubMenu:
    return await SubmenuService.update(
        menu_id,
        submenu_id,
        new_data,
        background_task,
    )


@router.delete(Submenu.LONG_LINK)
async def delete_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    background_task: BackgroundTasks,
) -> dict[str, bool | str]:
    return await SubmenuService.delete(menu_id, submenu_id, background_task)
