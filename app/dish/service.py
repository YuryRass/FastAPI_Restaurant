import uuid

from fastapi import BackgroundTasks, Response, status
from sqlalchemy.exc import IntegrityError

from app.dish.cache_dao import RedisDishDAO
from app.dish.dao import DishDAO
from app.dish.shemas import OutSDish, SDish
from app.exceptions import DishNotFoundException, SimilarDishTitlesException
from app.submenu.dao import SubmenuDAO


class DishService:
    """Сервисный слой для блюда."""

    @classmethod
    async def add(
        cls,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish: SDish,
        response: Response,
        background_task: BackgroundTasks,
    ) -> OutSDish:
        """Добавление блюда."""
        finded_submenu = await SubmenuDAO.show(menu_id, submenu_id)
        try:
            if finded_submenu:
                data = dish.model_dump(exclude_none=True)
                data.update(submenu_id=submenu_id)
                new_dish = await DishDAO.add(**data)
        except IntegrityError:
            raise SimilarDishTitlesException
        response.status_code = status.HTTP_201_CREATED
        added_dish = await DishDAO.show(menu_id, submenu_id, new_dish['id'])
        background_task.add_task(
            RedisDishDAO.create_update,
            added_dish,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=added_dish['id'],
        )
        return added_dish

    @classmethod
    async def show(
        cls,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        background_task: BackgroundTasks,
    ) -> OutSDish:
        """Отображение конкрентного блюда."""
        res = await RedisDishDAO.get(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )
        if res is not None:
            return res
        dish = await DishDAO.show(menu_id, submenu_id, dish_id)
        if not dish:
            raise DishNotFoundException
        background_task.add_task(
            RedisDishDAO.set,
            dish,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )

        return dish

    @classmethod
    async def show_all(
        cls,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        background_task: BackgroundTasks,
    ) -> list[OutSDish] | OutSDish:
        """Отображение всех блюд."""
        res = await RedisDishDAO.get_all(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        if res is not None:
            return res
        dishes = await DishDAO.show(menu_id, submenu_id)
        background_task.add_task(
            RedisDishDAO.set_all,
            dishes,
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
        return dishes

    @classmethod
    async def update(
        cls,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        new_data: SDish,
        background_task: BackgroundTasks,
    ) -> OutSDish:
        """Изменение блюда."""
        dish = await RedisDishDAO.get(
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=dish_id,
        )
        if dish is None:
            dish = await DishDAO.show(
                menu_id,
                submenu_id,
                dish_id,
            )
        if not dish:
            raise DishNotFoundException

        updated_dish = await DishDAO.update(
            dish_id, **new_data.model_dump(exclude_none=True)
        )

        new_dish = await DishDAO.show(menu_id, submenu_id, updated_dish['id'])
        background_task.add_task(
            RedisDishDAO.create_update,
            new_dish,
            menu_id=menu_id,
            submenu_id=submenu_id,
            dish_id=new_dish['id'],
        )
        return new_dish

    @classmethod
    async def delete(
        cls,
        menu_id: uuid.UUID,
        submenu_id: uuid.UUID,
        dish_id: uuid.UUID,
        background_task: BackgroundTasks,
    ) -> dict[str, bool | str]:
        """Удаление блюда."""
        deleted_dish = await DishDAO.delete_record(id=dish_id, submenu_id=submenu_id)
        if deleted_dish:
            background_task.add_task(
                RedisDishDAO.delete,
                menu_id=menu_id,
                submenu_id=submenu_id,
                dish_id=deleted_dish['id'],
            )
            return {'status': True, 'message': 'The dish has been deleted'}
        return {'status': False, 'message': 'Dish not found'}
