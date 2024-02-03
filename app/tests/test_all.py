from http import HTTPStatus
from typing import Any

from httpx import AsyncClient, Response


async def test_add_menu(
    menu_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка добавления нового меню."""
    response: Response = await ac.post(
        url='/menus',
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


async def test_add_submenu(
    submenu_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на добавление нового подменю."""
    menu = saved_data['menu']
    response: Response = await ac.post(
        url=f"/menus/{menu['id']}/submenus",
        json=submenu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, 'The response status is not 201'
    assert 'id' in response.json(), 'The submenu ID is not in the response'
    assert 'title' in response.json(), 'The submenu title is not in the response'
    assert (
        'description' in response.json()
    ), 'The submenu description is not in the response'

    assert 'dishes_count' in response.json(), 'The dishes_count is not in the response'
    assert (
        response.json()['title'] == submenu_post['title']
    ), 'The submenu title does not match the expected response'
    assert (
        response.json()['description'] == submenu_post['description']
    ), 'The submenu description does not match the expected response'

    saved_data['submenu'] = response.json()


async def test_add_first_dish(
    dish_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на добавление первого блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await ac.post(
        url=f"/menus/{menu['id']}/submenus/{submenu['id']}/dishes",
        json=dish_post,
    )
    assert response.status_code == HTTPStatus.CREATED, 'The response status is not 201'
    assert 'id' in response.json(), 'The dish ID is not in the response'
    assert 'title' in response.json(), 'The dish title is not in the response'
    assert (
        'description' in response.json()
    ), 'The dish description is not in the response'
    assert 'price' in response.json(), 'The dish price is not in the response'

    assert (
        response.json()['title'] == dish_post['title']
    ), 'The dish title does not match the expected response'
    assert (
        response.json()['description'] == dish_post['description']
    ), 'The dish description does not match the expected response'
    assert response.json()['price'] == '12.67'

    saved_data['dish'] = response.json()


async def test_add_second_dish(
    dish_2_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на добавление второго блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await ac.post(
        url=f"/menus/{menu['id']}/submenus/{submenu['id']}/dishes",
        json=dish_2_post,
    )
    assert response.status_code == HTTPStatus.CREATED, 'The response status is not 201'
    assert 'id' in response.json(), 'The dish ID is not in the response'
    assert 'title' in response.json(), 'The dish title is not in the response'
    assert (
        'description' in response.json()
    ), 'The dish description is not in the response'
    assert 'price' in response.json(), 'The dish price is not in the response'

    assert (
        response.json()['title'] == dish_2_post['title']
    ), 'The dish title does not match the expected response'
    assert (
        response.json()['description'] == dish_2_post['description']
    ), 'The dish description does not match the expected response'
    assert response.json()['price'] == '654.12'

    saved_data['dish'] = response.json()


async def test_get_menu_by_id(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка получения меню по его ID."""
    menu = saved_data['menu']
    response: Response = await ac.get(url=f"/menus/{menu['id']}")
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
        response.json()['submenus_count'] == 1
    ), 'The submenu_counts does not match the expected response'
    assert (
        response.json()['dishes_count'] == 2
    ), 'The dishes_count does not match the expected response'


async def test_get_submenu_by_id(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Получение созданного подменю по его ID."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response: Response = await ac.get(
        url=f"/menus/{menu['id']}/submenus/{submenu['id']}",
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert (
        response.json()['id'] == submenu['id']
    ), 'The submenu ID does not match the expected response'
    assert (
        response.json()['title'] == submenu['title']
    ), 'The submenu title does not match the expected response'
    assert (
        response.json()['description'] == submenu['description']
    ), 'The submenu description does not match the expected response'
    assert (
        response.json()['dishes_count'] == 2
    ), 'The dishes_count does not match the expected response'


async def test_delete_submenu(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на удаление созданного подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response: Response = await ac.delete(
        url=f"/menus/{menu['id']}/submenus/{submenu['id']}"
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert (
        response.json()['message'] == 'The submenu has been deleted'
    ), 'The deletion message does not match the expected on'


async def test_submenu_empty(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка получения пустого списка подменю."""
    menu = saved_data['menu']
    response: Response = await ac.get(url=f"/menus/{menu['id']}/submenus")
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert response.json() == [], 'There is a non-empty list in the response'


async def test_dish_empty(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка получения пустого списка блюд."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await ac.get(url=f"/menus/{menu['id']}/submenus/{submenu['id']}/dishes")
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert response.json() == [], 'There is an empty list in the response'


async def test_get_menu_by_id_not_empty(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка получения меню по его ID."""
    menu = saved_data['menu']
    response: Response = await ac.get(url=f"/menus/{menu['id']}")
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


async def test_delete_menu(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на удаление меню."""
    menu = saved_data['menu']
    response: Response = await ac.delete(
        url=f"/menus/{menu['id']}",
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert (
        response.json()['message'] == 'The menu has been deleted'
    ), 'The deletion message does not match the expected response'


async def test_menus_is_empty(ac: AsyncClient) -> None:
    """Проверка на пустое меню."""
    response: Response = await ac.get(
        url='/menus',
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert response.json() == [], 'There is a non-empty list in the response'
