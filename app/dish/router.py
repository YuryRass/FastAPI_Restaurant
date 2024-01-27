import uuid

from fastapi import APIRouter, Response, status
from sqlalchemy.exc import IntegrityError

from app.dish.dao import DishDAO
from app.dish.shemas import OutSDish, SDish
from app.exceptions import DishNotFoundException, SimilarDishTitlesException
from app.submenu.dao import SubmenuDAO

router: APIRouter = APIRouter(
    prefix="/menus",
    tags=["Dishes"],
)


@router.post("/{menu_id}/submenus/{submenu_id}/dishes")
async def add_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish: SDish,
    responce: Response,
):
    finded_submenu = await SubmenuDAO.show(menu_id, submenu_id)
    try:
        if finded_submenu:
            new_dish = await DishDAO.add(
                title=dish.title,
                description=dish.description,
                price=dish.price,
                submenu_id=submenu_id,
            )
    except IntegrityError:
        raise SimilarDishTitlesException
    responce.status_code = status.HTTP_201_CREATED
    added_dish = await DishDAO.show(menu_id, submenu_id, new_dish["id"])
    return OutSDish(**added_dish)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def show_dish_by_id(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
):
    dish = await DishDAO.show(menu_id, submenu_id, dish_id)

    if not dish:
        raise DishNotFoundException

    return OutSDish(**dish)


@router.get("/{menu_id}/submenus/{submenu_id}/dishes")
async def show_dishes(menu_id: uuid.UUID, submenu_id: uuid.UUID):
    dishes = await DishDAO.show(menu_id, submenu_id)

    return dishes


@router.patch("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def update_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
    new_data: SDish,
):
    dish = await DishDAO.show(menu_id, submenu_id, dish_id)
    if not dish:
        raise DishNotFoundException

    updated_dish = await DishDAO.update(
        dish_id,
        title=new_data.title,
        description=new_data.description,
        price=new_data.price,
    )

    dish = await DishDAO.show(menu_id, submenu_id, updated_dish["id"])

    return OutSDish(**dish)


@router.delete("/{menu_id}/submenus/{submenu_id}/dishes/{dish_id}")
async def delete_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
):
    dish = await DishDAO.show(menu_id, submenu_id, dish_id)
    if dish:
        await DishDAO.delete_record(id=dish_id, submenu_id=submenu_id)
        return {"status": True, "message": "The dish has been deleted"}
