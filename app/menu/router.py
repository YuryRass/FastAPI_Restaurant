from fastapi import APIRouter
from sqlalchemy import RowMapping
from app.menu.dao import MenuDAO
from app.migrations.env import target_metadata
import uuid

router: APIRouter = APIRouter(prefix="/menus")


@router.post("")
async def add_menu(title: str, description: str):
    menu: RowMapping = await MenuDAO.add(title=title, description=description)

    added_menu: RowMapping = await MenuDAO.show(id=menu["id"])

    return added_menu


@router.get("")
async def show_menus():
    menus = await MenuDAO.show()

    return menus


@router.get("{menu_id}")
async def show_menu_by_id(menu_id: uuid.UUID):
    menu: RowMapping = await MenuDAO.show(id=menu_id)

    return menu