import uuid

from fastapi import APIRouter, Response, status
from sqlalchemy.exc import IntegrityError

from app.exceptions import SimilarSubmenuTitlesException, SubMenuNotFoundException
from app.submenu.dao import SubmenuDAO
from app.submenu.shemas import OutSSubMenu, SSubMenu

router: APIRouter = APIRouter(
    prefix="/menus",
    tags=["Submenus"],
)


@router.post("/{menu_id}/submenus")
async def add_submenu(
    menu_id: uuid.UUID, menu: SSubMenu, responce: Response
) -> OutSSubMenu:
    try:
        submenu = await SubmenuDAO.add(
            title=menu.title,
            description=menu.description,
            menu_id=menu_id,
        )
    except IntegrityError:
        raise SimilarSubmenuTitlesException
    responce.status_code = status.HTTP_201_CREATED
    added_submenu = await SubmenuDAO.show(menu_id, submenu["id"])
    return added_submenu


@router.get("/{menu_id}/submenus/{submenu_id}")
async def show_submenu_by_id(menu_id: uuid.UUID, submenu_id: uuid.UUID) -> OutSSubMenu:
    submenu = await SubmenuDAO.show(menu_id, submenu_id)
    if not submenu:
        raise SubMenuNotFoundException

    return submenu


@router.get("/{menu_id}/submenus")
async def show_submenus(menu_id: uuid.UUID) -> list[OutSSubMenu] | OutSSubMenu:
    sub_menus = await SubmenuDAO.show(menu_id)

    return sub_menus


@router.patch("/{menu_id}/submenus/{submenu_id}")
async def update_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    new_data: SSubMenu,
) -> OutSSubMenu:
    submenu = await SubmenuDAO.show(menu_id, submenu_id)
    if not submenu:
        raise SubMenuNotFoundException

    updated_submenu = await SubmenuDAO.update(
        submenu_id,
        title=new_data.title,
        description=new_data.description,
    )

    submenu_res = await SubmenuDAO.show(menu_id, updated_submenu["id"])

    return submenu_res


@router.delete("/{menu_id}/submenus/{submenu_id}")
async def delete_submenu(
    menu_id: uuid.UUID, submenu_id: uuid.UUID
) -> dict[str, bool | str]:
    menu = await SubmenuDAO.delete_record(id=submenu_id, menu_id=menu_id)
    if menu:
        return {"status": True, "message": "The submenu has been deleted"}
