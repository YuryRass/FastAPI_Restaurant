import uuid

from fastapi import APIRouter, BackgroundTasks, Response

from app.dish.model import Dish
from app.dish.service import DishService
from app.dish.shemas import OutSDish, SDish

router: APIRouter = APIRouter(tags=['Dishes'])


@router.post(Dish.LINK)
async def add_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish: SDish,
    responce: Response,
    background_task: BackgroundTasks,
) -> OutSDish:
    """
    **Добавление блюда.**

    Args:
    - **menu_id (uuid.UUID)**: ID меню
    - **submenu_id (uuid.UUID)**: ID подменю
    - **dish (SDish)**: данные о новом блюде (title, description)

    Returns:
    - **OutSDish**: информация о добавленном блюде
    """
    return await DishService.add(
        menu_id,
        submenu_id,
        dish,
        responce,
        background_task,
    )


@router.get(Dish.LONG_LINK)
async def show_dish_by_id(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
    background_task: BackgroundTasks,
) -> OutSDish:
    """
    **Отображение блюда.**

    Args:
    - **menu_id (uuid.UUID)**: ID меню
    - **submenu_id (uuid.UUID)**: ID подменю
    - **dish_id (uuid.UUID)**: ID блюда

    Returns:
    - **OutSDish**: найденное блюдо
    """
    return await DishService.show(menu_id, submenu_id, dish_id, background_task)


@router.get(Dish.LINK)
async def show_dishes(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    background_task: BackgroundTasks,
) -> list[OutSDish]:
    """
    **Отображение всех блюд.**

    Args:
    - **menu_id (uuid.UUID)**: ID меню
    - **submenu_id (uuid.UUID)**: ID подменю

    Returns:
    - **list[OutSDish]**: список блюд
    """
    return await DishService.show_all(menu_id, submenu_id, background_task)


@router.patch(Dish.LONG_LINK)
async def update_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
    new_data: SDish,
    background_task: BackgroundTasks,
) -> OutSDish:
    """
    **Изменение блюда.**

    Args:
    - **menu_id (uuid.UUID)**: ID меню
    - **submenu_id (uuid.UUID)**: ID подменю
    - **dish_id (uuid.UUID)**: ID блюда
    - **new_data (SDish)**: новые данные для блюда

    Returns:
    - **OutSDish**: новое блюдо
    """
    return await DishService.update(
        menu_id,
        submenu_id,
        dish_id,
        new_data,
        background_task,
    )


@router.delete(Dish.LONG_LINK)
async def delete_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
    background_task: BackgroundTasks,
) -> dict[str, bool | str]:
    """
    **Удаление блюда.**

    Args:
    - **menu_id (uuid.UUID)**: ID меню
    - **submenu_id (uuid.UUID)**: ID подменю
    - **dish_id (uuid.UUID)**: ID блюда

    Returns:
    - **dict[str, bool | str]**: информация об удалении
    """
    return await DishService.delete(
        menu_id,
        submenu_id,
        dish_id,
        background_task,
    )
