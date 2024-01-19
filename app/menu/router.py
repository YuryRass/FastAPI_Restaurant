import uuid
from fastapi import APIRouter, Response, status
from sqlalchemy import RowMapping
from app.exceptions import MenuNotFoundException
from app.menu.dao import MenuDAO
from app.menu.model import Menu
from app.menu.shemas import SMenu

router: APIRouter = APIRouter(prefix="/menus")


@router.post("")
async def add_menu(menu: SMenu, responce: Response):
    menu: RowMapping = await MenuDAO.add(title=menu.title, description=menu.description)
    responce.status_code = status.HTTP_201_CREATED
    added_menu: RowMapping = await MenuDAO.show_menu(id=menu["id"])
    return added_menu


@router.get("")
async def show_menus():
    menus = await MenuDAO.show_menu()

    return menus


@router.get("/{menu_id}")
async def show_menu_by_id(menu_id: uuid.UUID):
    menu: RowMapping | None = await MenuDAO.show_menu(id=menu_id)
    if not menu:
        raise MenuNotFoundException

    return menu


@router.patch("/{menu_id}")
async def update_menu(menu_id: uuid.UUID, new_data: SMenu):
    menu: RowMapping | None = await MenuDAO.show_menu(id=menu_id)
    if not menu:
        raise MenuNotFoundException

    updated_menu: RowMapping = await MenuDAO.update(
        menu_id,
        title=new_data.title,
        description=new_data.description,
    )

    menu_res = await MenuDAO.show_menu(id=updated_menu["id"])

    return menu_res


@router.delete("/{menu_id}")
async def delete_menu(menu_id: uuid.UUID):
    menu = await MenuDAO.delete_record(id=menu_id)
    if menu:
        return {"status": True, "message": "The menu has been deleted"}
