import uuid

from fastapi import APIRouter, BackgroundTasks, Response

from app.submenu.model import Submenu
from app.submenu.service import SubmenuService
from app.submenu.shemas import OutSSubMenu, SSubMenu

router: APIRouter = APIRouter(tags=['Submenus'])


@router.post(
    Submenu.LINK,
    response_model=OutSSubMenu,
    responses={
        201: {
            'description': 'Submenu added successfully.',
            'content': {
                'application/json': {
                    'example': {
                        'id': '52777d1c-04b3-4a5a-9f1f-43e212ed0c2a',
                        'title': 'Новое подменю',
                        'description': 'Описание нового подменю',
                        'dishes_count': 0
                    }
                }
            }
        },
        400: {
            'description': 'Submenu titles must be unique.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Submenu titles must be unique'
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
async def add_submenu(
    menu_id: uuid.UUID,
    menu: SSubMenu,
    response: Response,
    background_task: BackgroundTasks,
) -> OutSSubMenu:
    """
    **Добавление подменю.**

    Этот endpoint позволяет добавить новое подменю.

    **Parameters:**
    - `menu_id (uuid.UUID)`: ID меню
    - `menu (SSubMenu)`: Данные о новом подменю

    **Returns:**
    - `OutSSubMenu`: Добавленное подменю

    **Responses:**
    - `201 Created`: Submenu added successfully.
        Example Response (201 Created):
        ```json
        {
            "id": "52777d1c-04b3-4a5a-9f1f-43e212ed0c2a",
            "title": "Новое подменю",
            "description": "Описание нового подменю",
            "dishes_count": 0
        }
        ```
    - `400 Bad Request`: Submenu titles must be unique.
        Example Response (400 Bad Request):
        ```json
        {
            "detail": "Submenu titles must be unique"
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
    return await SubmenuService.add(menu_id, menu, response, background_task)


@router.get(
    Submenu.LONG_LINK,
    response_model=OutSSubMenu,
    responses={
        200: {
            'description': 'Подменю найдено успешно.',
            'content': {
                'application/json': {
                    'example': {
                        'id': '52777d1c-04b3-4a5a-9f1f-43e212ed0c2a',
                        'title': 'Новое подменю',
                        'description': 'Описание нового подменю',
                        'dishes_count': 0
                    }
                }
            }
        },
        404: {
            'description': 'Подменю не найдено.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Подменю не найдено'
                    }
                }
            }
        },
        500: {
            'description': 'Внутренняя ошибка сервера.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Внутренняя ошибка сервера'
                    }
                }
            }
        },
    }
)
async def show_submenu_by_id(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    background_task: BackgroundTasks,
) -> OutSSubMenu:
    """
    **Отображение подменю.**

    Этот endpoint позволяет получить информацию о подменю по его ID.

    **Parameters:**
    - `menu_id (uuid.UUID)`: Уникальный идентификатор меню, к которому принадлежит подменю.
    - `submenu_id (uuid.UUID)`: Уникальный идентификатор подменю.

    **Returns:**
    - `OutSSubMenu`: Найденное подменю

    **Responses:**
    - `200 OK`: Подменю найдено успешно.
        Example Response (200 OK):
        ```json
        {
            "id": "52777d1c-04b3-4a5a-9f1f-43e212ed0c2a",
            "title": "Новое подменю",
            "description": "Описание нового подменю",
            "dishes_count": 0
        }
        ```
    - `404 Not Found`: submenu not found.
        Example Response (404 Not Found):
        ```json
        {
            "detail": "submenu not found"
        }
        ```
    - `500 Internal Server Error`: Внутренняя ошибка сервера.
        Example Response (500 Internal Server Error):
        ```json
        {
            "detail": "Внутренняя ошибка сервера"
        }
        ```

    """
    return await SubmenuService.show(menu_id, submenu_id, background_task)


@router.get(
    Submenu.LINK,
    response_model=list[OutSSubMenu] | OutSSubMenu,
    responses={
        200: {
            'description': 'Подменю найдено успешно.',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'id': '52777d1c-04b3-4a5a-9f1f-43e212ed0c2a',
                            'title': 'Новое подменю',
                            'description': 'Описание нового подменю',
                            'dishes_count': 0
                        }
                    ]
                }
            }
        },
        404: {
            'description': 'submenu not found.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'submenu not found'
                    }
                }
            }
        },
        500: {
            'description': 'Внутренняя ошибка сервера.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Внутренняя ошибка сервера'
                    }
                }
            }
        },
    }
)
async def show_submenus(
    menu_id: uuid.UUID,
    background_task: BackgroundTasks,
) -> list[OutSSubMenu] | OutSSubMenu:
    """
    **Отображение всех подменю.**

    Этот endpoint позволяет получить информацию о всех подменю, принадлежащих определенному меню.

    **Parameters:**
    - `menu_id (uuid.UUID)`: Уникальный идентификатор меню, для которого требуется отобразить подменю.

    **Returns:**
    - `list[OutSSubMenu] | OutSSubMenu`: Список подменю

    **Responses:**
    - `200 OK`: Подменю найдено успешно.
        Example Response (200 OK):
        ```json
        [
            {
                "id": "52777d1c-04b3-4a5a-9f1f-43e212ed0c2a",
                "title": "Новое подменю",
                "description": "Описание нового подменю",
                "dishes_count": 0
            }
        ]
        ```
    - `404 Not Found`: Подменю не найдено.
        Example Response (404 Not Found):
        ```json
        {
            "detail": "Подменю не найдено"
        }
        ```
    - `500 Internal Server Error`: Внутренняя ошибка сервера.
        Example Response (500 Internal Server Error):
        ```json
        {
            "detail": "Внутренняя ошибка сервера"
        }
        ```

    """
    return await SubmenuService.show_all(menu_id, background_task)


@router.patch(
    Submenu.LONG_LINK,
    response_model=OutSSubMenu,
    responses={
        200: {
            'description': 'Подменю успешно обновлено.',
            'content': {
                'application/json': {
                    'example': {
                        'id': '52777d1c-04b3-4a5a-9f1f-43e212ed0c2a',
                        'title': 'Измененное подменю',
                        'description': 'Обновленное описание подменю',
                        'dishes_count': 0
                    }
                }
            }
        },
        404: {
            'description': 'submenu not found.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'submenu not found'
                    }
                }
            }
        },
        500: {
            'description': 'Внутренняя ошибка сервера.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Внутренняя ошибка сервера'
                    }
                }
            }
        },
    }
)
async def update_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    new_data: SSubMenu,
    background_task: BackgroundTasks,
) -> OutSSubMenu:
    """
    **Изменение подменю.**

    Этот endpoint позволяет обновить данные о существующем подменю.

    **Parameters:**
    - `menu_id (uuid.UUID)`: Уникальный идентификатор меню, которому принадлежит подменю.
    - `submenu_id (uuid.UUID)`: Уникальный идентификатор подменю, которое требуется обновить.
    - `new_data (SSubMenu)`: Новые данные о подменю.

    **Returns:**
    - `OutSSubMenu`: Обновленное подменю.

    **Responses:**
    - `200 OK`: Подменю успешно обновлено.
        Example Response (200 OK):
        ```json
        {
            "id": "52777d1c-04b3-4a5a-9f1f-43e212ed0c2a",
            "title": "Измененное подменю",
            "description": "Обновленное описание подменю",
            "dishes_count": 0
        }
        ```
    - `404 Not Found`: Подменю не найдено.
        Example Response (404 Not Found):
        ```json
        {
            "detail": "Подменю не найдено"
        }
        ```
    - `500 Internal Server Error`: Внутренняя ошибка сервера.
        Example Response (500 Internal Server Error):
        ```json
        {
            "detail": "Внутренняя ошибка сервера"
        }
        ```

    """
    return await SubmenuService.update(
        menu_id,
        submenu_id,
        new_data,
        background_task,
    )


@router.delete(
    Submenu.LONG_LINK,
    response_model=dict[str, bool | str],
    responses={
        200: {
            'description': 'The submenu has been deleted.',
            'content': {
                'application/json': {
                    'example': {
                        'status': True,
                        'message': 'The submenu has been deleted'
                    }
                }
            }
        },
        404: {
            'description': 'Submenu not found.',
            'content': {
                'application/json': {
                    'example': {
                        'status': False,
                        'message': 'Submenu not found'
                    }
                }
            }
        },
        500: {
            'description': 'Внутренняя ошибка сервера.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Внутренняя ошибка сервера'
                    }
                }
            }
        },
    }
)
async def delete_submenu(
    menu_id: uuid.UUID,
    submenu_id: uuid.UUID,
    background_task: BackgroundTasks,
) -> dict[str, bool | str]:
    """
    **Удаление подменю.**

    Этот endpoint позволяет удалить существующее подменю.

    **Parameters:**
    - `menu_id (uuid.UUID)`: Уникальный идентификатор меню, которому принадлежит подменю.
    - `submenu_id (uuid.UUID)`: Уникальный идентификатор подменю, которое требуется удалить.

    **Returns:**
    - `dict[str, bool | str]`: Информация об удалении. Если удаление прошло успешно, будет возвращено `{'status': True, 'message': 'Подменю успешно удалено'}`, иначе `{'status': False, 'message': 'Подменю не найдено'}`.

    **Responses:**
    - `200 OK`: The submenu has been deleted.
        Example Response (200 OK):
        ```json
        {
            "status": True,
            "message": "The submenu has been deleted"
        }
        ```
    - `404 Not Found`: Submenu not found.
        Example Response (404 Not Found):
        ```json
        {
            "status": False,
            "message": "Submenu not found"
        }
        ```
    - `500 Internal Server Error`: Внутренняя ошибка сервера.
        Example Response (500 Internal Server Error):
        ```json
        {
            "detail": "Внутренняя ошибка сервера"
        }
        ```

    """
    return await SubmenuService.delete(menu_id, submenu_id, background_task)
