import uuid

from fastapi import APIRouter, BackgroundTasks, Response

from app.dish.model import Dish
from app.dish.service import DishService
from app.dish.shemas import OutSDish, SDish

router: APIRouter = APIRouter(tags=['Dishes'])


@router.post(
    Dish.LINK,
    response_model=OutSDish,
    responses={
        201: {
            'description': 'Блюдо успешно добавлено',
            'content': {'application/json': {'example': {'title': 'Цезарь', 'description': 'Классический салат Цезарь с курицей', 'price': 7.99, 'id': 'a1b2c3d4-1234-5678-9abc-def012345678'}}}
        },
        400: {
            'description': 'Bad Request',
            'content': {'application/json': {'example': {'detail': 'Dish titles must be unique'}}}
        },
        500: {
            'description': 'Internal server error.',
            'content': {'application/json': {'example': {'detail': 'Dish titles must be unique'}}},
        }
    })
async def add_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish: SDish,
    response: Response,
    background_task: BackgroundTasks,
) -> OutSDish:
    """
    **Добавление блюда.**

    Этот endpoint позволяет добавить новое блюдо в подменю меню.

    **Parameters:**
    - `menu_id (uuid.UUID)`: ID меню
    - `submenu_id (uuid.UUID)`: ID подменю
    - `dish (SDish)`: Данные о новом блюде (title, description, price)

    **Returns:**
    - `OutSDish`: Информация о добавленном блюде

    **Responses:**
    - `201 Created`: Блюдо успешно добавлено.
    - `400 Bad Request`: Не удалось добавить блюдо из-за дублирования названия.

    **Example Request:**
    ```http
    POST /dishes/menu_id/submenu_id
    Content-Type: application/json

    {
        "title": "Цезарь",
        "description": "Классический салат Цезарь с курицей",
        "price": 7.99
    }
    ```

    **Example Response (201 Created):**
    ```json
    {
        "id": "c9e3ddbb-0df3-4654-9e44-4a4472a7a52c",
        "title": "Цезарь",
        "description": "Классический салат Цезарь с курицей",
        "price": "7.99"
    }
    ```

    **Example Response (400 Bad Request):**
    ```json
    {
        "detail": "Dish titles must be unique"
    }
    ```

    """
    return await DishService.add(
        menu_id,
        submenu_id,
        dish,
        response,
        background_task,
    )


@router.get(
    Dish.LONG_LINK,
    response_model=OutSDish,
    responses={
        200: {
            'description': 'Dish information retrieved successfully.',
            'content': {
                'application/json': {
                    'example': {
                        'id': '52777d1c-04b3-4a5a-9f1f-43e212ed0c2a',
                        'title': 'Цезарь',
                        'description': 'Классический салат Цезарь с курицей',
                        'price': '7.99'
                    }
                }
            }
        },
        404: {
            'description': 'Dish not found.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Dish not found'
                    }
                }
            }
        },
        500: {
            'description': 'Internal server error.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Internal server error'
                    }
                }
            }
        },
    }
)
async def show_dish_by_id(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
    background_task: BackgroundTasks,
) -> OutSDish:
    """
    **Отображение блюда.**

    Этот endpoint позволяет получить информацию о конкретном блюде по его идентификатору.

    **Parameters:**
    - `menu_id (uuid.UUID)`: ID меню
    - `submenu_id (uuid.UUID)`: ID подменю
    - `dish_id (uuid.UUID)`: ID блюда

    **Returns:**
    - `OutSDish`: Найденное блюдо

    **Responses:**
    - `200 OK`: Dish information retrieved successfully.
        Example Response (200 OK):
        ```json
        {
            "id": "52777d1c-04b3-4a5a-9f1f-43e212ed0c2a",
            "title": "Цезарь",
            "description": "Классический салат Цезарь с курицей",
            "price": "7.99"
        }
        ```
    - `404 Not Found`: Dish not found.
        Example Response (404 Not Found):
        ```json
        {
            "detail": "Dish not found"
        }
        ```
    - `500 Internal Server Error`: Internal server error.
        Example Response (500 Internal Server Error):
        ```json
        {
            "detail": "Internal server error"
        }
        ```

    """
    return await DishService.show(menu_id, submenu_id, dish_id, background_task)


@router.get(
    Dish.LINK,
    response_model=list[OutSDish],
    responses={
        200: {
            'description': 'Dishes information retrieved successfully.',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'id': '52777d1c-04b3-4a5a-9f1f-43e212ed0c2a',
                            'title': 'Цезарь',
                            'description': 'Классический салат Цезарь с курицей',
                            'price': '7.99'
                        },
                        {
                            'id': 'f49a3c9d-6e8d-4e1a-b22a-8ac9868085a6',
                            'title': 'Греческий салат',
                            'description': 'Овощной салат с фетой и оливками',
                            'price': '6.49'
                        }
                    ]
                }
            }
        },
        404: {
            'description': 'Submenu not found.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Submenu not found'
                    }
                }
            }
        },
        500: {
            'description': 'Internal server error.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Internal server error'
                    }
                }
            }
        },
    }
)
async def show_dishes(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    background_task: BackgroundTasks,
) -> list[OutSDish]:
    """
    **Отображение всех блюд.**

    Этот endpoint позволяет получить информацию обо всех блюдах в определенном подменю.

    **Parameters:**
    - `menu_id (uuid.UUID)`: ID меню
    - `submenu_id (uuid.UUID)`: ID подменю

    **Returns:**
    - `list[OutSDish]`: Список блюд

    **Responses:**
    - `200 OK`: Dishes information retrieved successfully.
        Example Response (200 OK):
        ```json
        [
            {
                "id": "52777d1c-04b3-4a5a-9f1f-43e212ed0c2a",
                "title": "Цезарь",
                "description": "Классический салат Цезарь с курицей",
                "price": "7.99"
            },
            {
                "id": "f49a3c9d-6e8d-4e1a-b22a-8ac9868085a6",
                "title": "Греческий салат",
                "description": "Овощной салат с фетой и оливками",
                "price": "6.49"
            }
        ]
        ```
    - `404 Not Found`: Submenu not found.
        Example Response (404 Not Found):
        ```json
        {
            "detail": "Submenu not found"
        }
        ```
    - `500 Internal Server Error`: Internal server error.
        Example Response (500 Internal Server Error):
        ```json
        {
            "detail": "Internal server error"
        }
        ```

    """
    return await DishService.show_all(menu_id, submenu_id, background_task)


@router.patch(
    Dish.LONG_LINK,
    response_model=OutSDish,
    responses={
        200: {
            'description': 'Dish updated successfully.',
            'content': {
                'application/json': {
                    'example': {
                        'id': '52777d1c-04b3-4a5a-9f1f-43e212ed0c2a',
                        'title': 'Цезарь',
                        'description': 'Обновленное описание блюда',
                        'price': '8.99'
                    }
                }
            }
        },
        404: {
            'description': 'Dish not found.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Dish not found'
                    }
                }
            }
        },
        500: {
            'description': 'Internal server error.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Internal server error'
                    }
                }
            }
        },
    }
)
async def update_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
    new_data: SDish,
    background_task: BackgroundTasks,
) -> OutSDish:
    """
    **Изменение блюда.**

    Этот endpoint позволяет обновить информацию о конкретном блюде по его идентификатору.

    **Parameters:**
    - `menu_id (uuid.UUID)`: ID меню
    - `submenu_id (uuid.UUID)`: ID подменю
    - `dish_id (uuid.UUID)`: ID блюда
    - `new_data (SDish)`: Новые данные для блюда

    **Returns:**
    - `OutSDish`: Новое блюдо

    **Responses:**
    - `200 OK`: Dish updated successfully.
        Example Response (200 OK):
        ```json
        {
            "id": "52777d1c-04b3-4a5a-9f1f-43e212ed0c2a",
            "title": "Цезарь",
            "description": "Обновленное описание блюда",
            "price": "8.99"
        }
        ```
    - `404 Not Found`: Dish not found.
        Example Response (404 Not Found):
        ```json
        {
            "detail": "Dish not found"
        }
        ```
    - `500 Internal Server Error`: Internal server error.
        Example Response (500 Internal Server Error):
        ```json
        {
            "detail": "Internal server error"
        }
        ```

    """
    return await DishService.update(
        menu_id,
        submenu_id,
        dish_id,
        new_data,
        background_task,
    )


@router.delete(
    Dish.LONG_LINK,
    response_model=dict[str, bool | str],
    responses={
        200: {
            'description': 'Dish deleted successfully.',
            'content': {
                'application/json': {
                    'example': {
                        'status': True,
                        'message': 'The dish has been deleted'
                    }
                }
            }
        },
        404: {
            'description': 'Dish not found.',
            'content': {
                'application/json': {
                    'example': {
                        'status': False,
                        'message': 'Dish not found'
                    }
                }
            }
        },
        500: {
            'description': 'Internal server error.',
            'content': {
                'application/json': {
                    'example': {
                        'status': False,
                        'message': 'Internal server error'
                    }
                }
            }
        },
    }
)
async def delete_dish(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    dish_id: uuid.UUID,
    background_task: BackgroundTasks,
) -> dict[str, bool | str]:
    """
    **Удаление блюда.**

    Этот endpoint позволяет удалить конкретное блюдо по его идентификатору.

    **Parameters:**
    - `menu_id (uuid.UUID)`: ID меню
    - `submenu_id (uuid.UUID)`: ID подменю
    - `dish_id (uuid.UUID)`: ID блюда

    **Returns:**
    - `dict[str, bool | str]`: Информация об удалении

    **Responses:**
    - `200 OK`: Dish deleted successfully.
        Example Response (200 OK):
        ```json
        {
            "status": true,
            "message": "The dish has been deleted"
        }
        ```
    - `404 Not Found`: Dish not found.
        Example Response (404 Not Found):
        ```json
        {
            "status": false,
            "message": "Dish not found"
        }
        ```
    - `500 Internal Server Error`: Internal server error.
        Example Response (500 Internal Server Error):
        ```json
        {
            "status": false,
            "message": "Internal server error"
        }
        ```

    """
    return await DishService.delete(
        menu_id,
        submenu_id,
        dish_id,
        background_task,
    )
