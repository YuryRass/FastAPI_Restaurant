import uuid
from http import HTTPStatus
from typing import Any

from httpx import AsyncClient, Response

from app.menu.router import (
    add_menu,
    delete_menu,
    show_menu_by_id,
    show_menus,
    update_menu,
)
from app.utils.url import reverse


async def test_menus_is_empty(ac: AsyncClient) -> None:
    """Проверка на пустое меню."""
    response: Response = await ac.get(url=reverse(show_menus))
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert response.json() == [], 'There is a non-empty list in the response'


async def test_add_menu(
    menu_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка добавления нового меню."""
    response: Response = await ac.post(
        url=reverse(add_menu),
        json=menu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, 'The response status is not 201'
    assert 'id' in response.json(), 'The menu ID is not in the response'
    assert 'title' in response.json(), 'The menu title is not in the response'
    assert (
        'description' in response.json()
    ), 'The menu description is not in the response'
    assert (
        'submenus_count' in response.json()
    ), 'The submenus_count is not in the response'
    assert 'dishes_count' in response.json(), 'The dishes_count is not in the response'
    assert (
        response.json()['title'] == menu_post['title']
    ), 'The menu title does not match the expected response'
    assert (
        response.json()['description'] == menu_post['description']
    ), 'The menu description does not match the expected response'

    saved_data['menu'] = response.json()


async def test_add_menu_similar(
    menu_post: dict[str, str],
    ac: AsyncClient,
) -> None:
    """Проверка на добавление нового меню с одинаковым названием."""
    response: Response = await ac.post(
        url=reverse(add_menu),
        json=menu_post,
    )
    assert (
        response.status_code == HTTPStatus.BAD_REQUEST
    ), 'The response status is not 400'


async def test_menus_not_empty(ac: AsyncClient) -> None:
    """Проверка на получение непустого списка меню."""
    response: Response = await ac.get(url=reverse(show_menus))
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert response.json() != [], 'There is an empty list in the response'


async def test_get_menu_by_id(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка получения меню по его ID."""
    menu = saved_data['menu']
    response: Response = await ac.get(url=reverse(show_menu_by_id, menu_id=menu['id']))
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert (
        response.json()['id'] == menu['id']
    ), 'The menu ID does not match the expected response'
    assert (
        response.json()['title'] == menu['title']
    ), 'The menu title does not match the expected response'
    assert (
        response.json()['description'] == menu['description']
    ), 'The menu description does not match the expected response'
    assert (
        response.json()['submenus_count'] == 0
    ), 'The submenu_counts does not match the expected response'
    assert (
        response.json()['dishes_count'] == 0
    ), 'The dishes_count does not match the expected response'


async def test_update_menu(
    menu_patch: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на изменение данных о меню."""
    menu = saved_data['menu']
    response: Response = await ac.patch(
        url=reverse(update_menu, menu_id=menu['id']),
        json=menu_patch,
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert 'id' in response.json(), 'The menu ID is not in the response'
    assert 'title' in response.json(), 'The menu title is not in the response'
    assert (
        'description' in response.json()
    ), 'The menu description is not in the response'
    assert (
        'submenus_count' in response.json()
    ), 'The submenus_count is not in the response'
    assert 'dishes_count' in response.json(), 'The dishes_count is not in the response'
    assert (
        response.json()['title'] == menu_patch['title']
    ), 'The menu title does not match the expected response'
    assert (
        response.json()['description'] == menu_patch['description']
    ), 'The menu description does not match the expected response'

    saved_data['menu'] = response.json()


async def test_update_non_existent_menu(
    non_existen_menu_id: uuid.UUID,
    menu_patch: dict[str, str],
    ac: AsyncClient,
) -> None:
    """Проверка на изменение несуществующего меню."""
    response: Response = await ac.patch(
        url=reverse(update_menu, menu_id=non_existen_menu_id),
        json=menu_patch,
    )

    assert response.status_code == HTTPStatus.NOT_FOUND


async def test_get_updated_menu_by_id(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка получения измененного меню."""
    menu = saved_data['menu']
    response: Response = await ac.get(
        url=reverse(show_menu_by_id, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert (
        response.json()['id'] == menu['id']
    ), 'The menu ID does not match the expected response'
    assert (
        response.json()['title'] == menu['title']
    ), 'The menu title does not match the expected response'
    assert (
        response.json()['description'] == menu['description']
    ), 'The menu description does not match the expected response'
    assert (
        response.json()['submenus_count'] == 0
    ), 'The submenu_counts does not match the expected response'
    assert (
        response.json()['dishes_count'] == 0
    ), 'The dishes_counts does not match the expected response'


async def test_delete_menu(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на удаление меню."""
    menu = saved_data['menu']
    response: Response = await ac.delete(
        url=reverse(delete_menu, menu_id=menu['id']),
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert (
        response.json()['message'] == 'The menu has been deleted'
    ), 'The deletion message does not match the expected response'


async def test_get_deleted_menu(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на отсутствие удаленного меню."""
    menu = saved_data['menu']
    response = await ac.get(url=reverse(show_menu_by_id, menu_id=menu['id']))
    assert (
        response.status_code == HTTPStatus.NOT_FOUND
    ), 'The response status is not 404'
    assert (
        response.json()['detail'] == 'menu not found'
    ), 'The error message does not match the expected response'
