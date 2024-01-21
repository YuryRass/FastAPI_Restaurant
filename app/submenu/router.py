import uuid

from fastapi import APIRouter, Response, status

from app.exceptions import SubMenuNotFoundException
from app.submenu.dao import SubmenuDAO
from app.submenu.shemas import SSubMenu

router: APIRouter = APIRouter(prefix="/menus")


@router.post("/{menu_id}/submenus")
async def add_submenu(menu_id: uuid.UUID, menu: SSubMenu, responce: Response):
    submenu = await SubmenuDAO.add(
        title=menu.title,
        description=menu.description,
        menu_id=menu_id,
    )
    responce.status_code = status.HTTP_201_CREATED
    added_submenu = await SubmenuDAO.show(id=submenu["id"])
    return added_submenu


@router.get("/{menu_id}/submenus/{submenu_id}")
async def show_submenu_by_id(menu_id: uuid.UUID, submenu_id: uuid.UUID):
    submenu = await SubmenuDAO.show(
        id=submenu_id,
        menu_id=menu_id,
    )
    if not submenu:
        raise SubMenuNotFoundException

    return submenu


@router.get("/{menu_id}/submenus")
async def show_submenus(menu_id: uuid.UUID):
    sub_menus = await SubmenuDAO.show(menu_id=menu_id)

    return sub_menus


@router.patch("/{menu_id}/submenus/{submenu_id}")
async def update_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    new_data: SSubMenu,
):
    submenu = await SubmenuDAO.show(
        id=submenu_id,
        menu_id=menu_id,
    )
    if not submenu:
        raise SubMenuNotFoundException

    updated_menu = await SubmenuDAO.update(
        submenu_id,
        title=new_data.title,
        description=new_data.description,
    )

    submenu_res = await SubmenuDAO.show(id=updated_menu["id"])

    return submenu_res


@router.delete("/{menu_id}/submenus/{submenu_id}")
async def delete_menu(menu_id: uuid.UUID, submenu_id: uuid.UUID):
    menu = await SubmenuDAO.delete_record(id=submenu_id, menu_id=menu_id)
    if menu:
        return {"status": True, "message": "The submenu has been deleted"}
