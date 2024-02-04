import uuid

from fastapi import APIRouter, BackgroundTasks, Response

from app.menu.model import Menu
from app.menu.service import MenuService
from app.menu.shemas import OutSMenu, SMenu

router: APIRouter = APIRouter(tags=['Menus'])


@router.post(
    Menu.LINK,
    response_model=OutSMenu,
    responses={
        201: {
            'description': 'Menu added successfully.',
            'content': {
                'application/json': {
                    'example': {
                        'id': '52777d1c-04b3-4a5a-9f1f-43e212ed0c2a',
                        'title': 'Новое меню',
                        'description': 'Описание нового меню',
                        'submenus_count': 0,
                        'dishes_count': 0
                    }
                }
            }
        },
        400: {
            'description': 'Menu title must be unique.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Menu title must be unique'
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
async def add_menu(
    menu: SMenu,
    response: Response,
    background_task: BackgroundTasks,
) -> OutSMenu:
    """
    **Добавление меню.**

    Этот endpoint позволяет добавить новое меню.

    **Parameters:**
    - `menu (SMenu)`: Данные о меню

    **Returns:**
    - `OutSMenu`: Добавленные данные о меню

    **Responses:**
    - `201 Created`: Menu added successfully.
        Example Response (201 Created):
        ```json
        {
            "id": "52777d1c-04b3-4a5a-9f1f-43e212ed0c2a",
            "title": "Новое меню",
            "description": "Описание нового меню",
            "submenus_count": 0,
            "dishes_count": 0
        }
        ```
    - `400 Bad Request`: menu titles must be unique.
        Example Response (400 Bad Request):
        ```json
        {
            "detail": "menu titles must be unique"
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
    return await MenuService.add(menu, response, background_task)


@router.get(
    Menu.LINK,
    response_model=list[OutSMenu],
    responses={
        200: {
            'description': 'Список всех меню успешно получен.',
            'content': {
                'application/json': {
                    'example': [
                        {
                            'id': '52777d1c-04b3-4a5a-9f1f-43e212ed0c2a',
                            'title': 'Меню 1',
                            'description': 'Описание меню 1',
                            'submenus_count': 3,
                            'dishes_count': 15
                        },
                        {
                            'id': '53a49ab3-ec2d-4a10-bc84-fa980ed7d8c3',
                            'title': 'Меню 2',
                            'description': 'Описание меню 2',
                            'submenus_count': 2,
                            'dishes_count': 10
                        }
                    ]
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
async def show_menus(background_task: BackgroundTasks) -> list[OutSMenu]:
    """
    **Получение списка всех меню.**

    Этот метод предоставляет список всех меню в системе.

    **Response (200 OK):**
    - **list[OutSMenu]**: Список всех меню в системе.

    Пример ответа (200 OK):
    ```json
    [
        {
            "id": "52777d1c-04b3-4a5a-9f1f-43e212ed0c2a",
            "title": "Меню 1",
            "description": "Описание меню 1",
            "submenus_count": 3,
            "dishes_count": 15
        },
        {
            "id": "53a49ab3-ec2d-4a10-bc84-fa980ed7d8c3",
            "title": "Меню 2",
            "description": "Описание меню 2",
            "submenus_count": 2,
            "dishes_count": 10
        }
    ]
    ```

    **Response (500 Internal Server Error):**
    - **detail** (str): Описание внутренней ошибки сервера.

    Пример ответа (500 Internal Server Error):
    ```json
    {
        "detail": "Внутренняя ошибка сервера"
    }
    ```

    **Responses:**
    - `200 OK`: Список всех меню успешно получен.
    - `500 Internal Server Error`: Внутренняя ошибка сервера.

    :param background_task: Фоновая задача для обновления данных.
    :type background_task: BackgroundTasks

    :return: Список всех меню в системе.
    :rtype: list[OutSMenu]
    """

    return await MenuService.show_all(background_task)


@router.get(
    Menu.LONG_LINK,
    response_model=OutSMenu,
    responses={
        200: {
            'description': 'Меню успешно получено.',
            'content': {
                'application/json': {
                    'example': {
                        'id': '52777d1c-04b3-4a5a-9f1f-43e212ed0c2a',
                        'title': 'Меню 1',
                        'description': 'Описание меню 1',
                        'submenus_count': 3,
                        'dishes_count': 15
                    }
                }
            }
        },
        404: {
            'description': 'menu not found.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'menu not found'
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
async def show_menu_by_id(
    menu_id: uuid.UUID, background_task: BackgroundTasks
) -> OutSMenu:
    """
    **Получение меню по его ID.**

    Этот метод позволяет получить информацию о меню по его уникальному идентификатору (ID).

    **Parameters:**
    - `menu_id (uuid.UUID)`: Уникальный идентификатор меню.

    **Response (200 OK):**
    - **OutSMenu**: Данные о найденном меню.

    Пример ответа (200 OK):
    ```json
    {
        "id": "52777d1c-04b3-4a5a-9f1f-43e212ed0c2a",
        "title": "Меню 1",
        "description": "Описание меню 1",
        "submenus_count": 3,
        "dishes_count": 15
    }
    ```

    **Response (404 Not Found):**
    - **detail** (str): Описание ошибки, если меню с указанным ID не найдено.

    Пример ответа (404 Not Found):
    ```json
    {
        "detail": "menu not found"
    }
    ```

    **Response (500 Internal Server Error):**
    - **detail** (str): Описание внутренней ошибки сервера.

    Пример ответа (500 Internal Server Error):
    ```json
    {
        "detail": "Внутренняя ошибка сервера"
    }
    ```

    **Responses:**
    - `200 OK`: Меню успешно получено.
    - `404 Not Found`: Меню не найдено.
    - `500 Internal Server Error`: Внутренняя ошибка сервера.

    :param menu_id: Уникальный идентификатор меню.
    :type menu_id: uuid.UUID
    :param background_task: Фоновая задача для обновления данных.
    :type background_task: BackgroundTasks

    :return: Данные о найденном меню.
    :rtype: OutSMenu
    """
    return await MenuService.show(menu_id, background_task)


@router.patch(
    Menu.LONG_LINK,
    response_model=OutSMenu,
    responses={
        200: {
            'description': 'Данные о меню успешно изменены.',
            'content': {
                'application/json': {
                    'example': {
                        'id': '52777d1c-04b3-4a5a-9f1f-43e212ed0c2a',
                        'title': 'Обновленное меню',
                        'description': 'Новое описание меню',
                        'submenus_count': 3,
                        'dishes_count': 15
                    }
                }
            }
        },
        404: {
            'description': 'Меню не найдено.',
            'content': {
                'application/json': {
                    'example': {
                        'detail': 'Меню не найдено'
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
async def update_menu(
    menu_id: uuid.UUID,
    new_data: SMenu,
    background_task: BackgroundTasks,
) -> OutSMenu:
    """
    **Изменение данных о меню.**

    Этот метод позволяет изменить данные о существующем меню.

    **Parameters:**
    - `menu_id (uuid.UUID)`: Уникальный идентификатор меню.
    - `new_data (SMenu)`: Новые данные о меню.

    **Response (200 OK):**
    - **OutSMenu**: Измененное меню.

    Пример ответа (200 OK):
    ```json
    {
        "id": "52777d1c-04b3-4a5a-9f1f-43e212ed0c2a",
        "title": "Обновленное меню",
        "description": "Новое описание меню",
        "submenus_count": 3,
        "dishes_count": 15
    }
    ```

    **Response (404 Not Found):**
    - **detail** (str): Описание ошибки, если меню с указанным ID не найдено.

    Пример ответа (404 Not Found):
    ```json
    {
        "detail": "Меню не найдено"
    }
    ```

    **Response (500 Internal Server Error):**
    - **detail** (str): Описание внутренней ошибки сервера.

    Пример ответа (500 Internal Server Error):
    ```json
    {
        "detail": "Внутренняя ошибка сервера"
    }
    ```

    **Responses:**
    - `200 OK`: Данные о меню успешно изменены.
    - `404 Not Found`: Меню не найдено.
    - `500 Internal Server Error`: Внутренняя ошибка сервера.

    :param menu_id: Уникальный идентификатор меню.
    :type menu_id: uuid.UUID
    :param new_data: Новые данные о меню.
    :type new_data: SMenu
    :param background_task: Фоновая задача для обновления данных.
    :type background_task: BackgroundTasks

    :return: Измененное меню.
    :rtype: OutSMenu
    """
    return await MenuService.update(menu_id, new_data, background_task)


@router.delete(
    Menu.LONG_LINK,
    response_model=dict[str, bool | str],
    responses={
        200: {
            'description': 'Меню успешно удалено.',
            'content': {
                'application/json': {
                    'example': {
                        'status': True,
                        'message': 'Меню успешно удалено'
                    }
                }
            }
        },
        404: {
            'description': 'Меню не найдено.',
            'content': {
                'application/json': {
                    'example': {
                        'status': False,
                        'message': 'Меню не найдено'
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
async def delete_menu(
    menu_id: uuid.UUID,
    background_task: BackgroundTasks,
) -> dict[str, bool | str]:
    """
    **Удаление меню.**

    Этот метод позволяет удалить существующее меню по его ID.

    **Parameters:**
    - `menu_id (uuid.UUID)`: Уникальный идентификатор меню.

    **Response (200 OK):**
    - **status** (bool): True, если меню успешно удалено; False, если меню не найдено.
    - **message** (str): Сообщение о результате операции удаления.

    Пример ответа (200 OK):
    ```json
    {
        "status": True,
        "message": "Меню успешно удалено"
    }
    ```

    **Response (404 Not Found):**
    - **status** (bool): False.
    - **message** (str): Сообщение о том, что меню не найдено.

    Пример ответа (404 Not Found):
    ```json
    {
        "status": False,
        "message": "Меню не найдено"
    }
    ```

    **Response (500 Internal Server Error):**
    - **detail** (str): Описание внутренней ошибки сервера.

    Пример ответа (500 Internal Server Error):
    ```json
    {
        "detail": "Внутренняя ошибка сервера"
    }
    ```

    **Responses:**
    - `200 OK`: Меню успешно удалено.
    - `404 Not Found`: Меню не найдено.
    - `500 Internal Server Error`: Внутренняя ошибка сервера.

    :param menu_id: Уникальный идентификатор меню.
    :type menu_id: uuid.UUID
    :param background_task: Фоновая задача для удаления данных.
    :type background_task: BackgroundTasks

    :return: Информация об удалении меню.
    :rtype: dict[str, bool | str]
    """
    return await MenuService.delete(menu_id, background_task)
