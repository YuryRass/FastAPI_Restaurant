import uuid

from fastapi import APIRouter, Response, status

from app.exceptions import MenuNotFoundException
from app.menu.dao import MenuDAO
from app.menu.shemas import SMenu

router: APIRouter = APIRouter(prefix="/menus")


@router.post("")
async def add_menu(menu: SMenu, responce: Response):
    menu_res = await MenuDAO.add(title=menu.title, description=menu.description)
    responce.status_code = status.HTTP_201_CREATED
    added_menu = await MenuDAO.show(id=menu_res["id"])
    return added_menu


@router.get("")
async def show_menus():
    menus = await MenuDAO.show()

    return menus


@router.get("/{menu_id}")
async def show_menu_by_id(menu_id: uuid.UUID):
    menu = await MenuDAO.show(id=menu_id)
    if not menu:
        raise MenuNotFoundException

    return menu


@router.patch("/{menu_id}")
async def update_menu(menu_id: uuid.UUID, new_data: SMenu):
    menu = await MenuDAO.show(id=menu_id)
    if not menu:
        raise MenuNotFoundException

    updated_menu = await MenuDAO.update(
        menu_id,
        title=new_data.title,
        description=new_data.description,
    )

    menu_res = await MenuDAO.show(id=updated_menu["id"])

    return menu_res


@router.delete("/{menu_id}")
async def delete_menu(menu_id: uuid.UUID):
    menu = await MenuDAO.delete_record(id=menu_id)
    if menu:
        return {"status": True, "message": "The menu has been deleted"}
