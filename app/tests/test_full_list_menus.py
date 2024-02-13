from http import HTTPStatus
from typing import Any

from httpx import AsyncClient, Response

from app.dish.router import add_dish, delete_dish
from app.menu.router import add_menu, delete_menu, show_full_list_menus, show_menus
from app.submenu.router import add_submenu, delete_submenu
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


async def test_add_submenu(
    submenu_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на добавление нового подменю."""
    menu = saved_data['menu']
    response: Response = await ac.post(
        url=reverse(add_submenu, menu_id=menu['id']),
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


async def test_add_dish(
    dish_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на добавление первого блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await ac.post(
        url=reverse(add_dish, menu_id=menu['id'], submenu_id=submenu['id']),
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


async def test_full_list_menus(
    menu_post: dict[str, str],
    submenu_post: dict[str, str],
    dish_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """
    Проверка вывода всех меню со всеми связанными подменю и блюдами.
    """
    response = await ac.get(url=reverse(show_full_list_menus))
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'

    data = response.json()

    assert len(data) == 1, 'There is more than one menu in the response'
    assert (
        data[0]['title'] == menu_post['title']
    ), 'The menu title does not match the expected response'
    assert (
        data[0]['description'] == menu_post['description']
    ), 'The menu description does not match the expected response'
    assert (
        data[0]['id'] == saved_data['menu']['id']
    ), 'The menu ID does not match the expected response'
    assert (
        len(data[0]['submenus']) == 1
    ), 'The submenus count does not match the expected response'

    submenu = data[0]['submenus'][0]

    assert (
        submenu['title'] == submenu_post['title']
    ), 'The submenu title does not match the expected response'
    assert (
        submenu['description'] == submenu_post['description']
    ), 'The submenu description does not match the expected response'
    assert (
        submenu['id'] == saved_data['submenu']['id']
    ), 'The submenu ID does not match the expected response'
    assert (
        len(submenu['dishes']) == 1
    ), 'The dishes count does not match the expected response'

    dish = submenu['dishes'][0]

    assert (
        dish['title'] == dish_post['title']
    ), 'The dish title does not match the expected response'
    assert (
        dish['description'] == dish_post['description']
    ), 'The dish description does not match the expected response'
    assert (
        dish['price'] == round(float(dish_post['price']), 2)
    ), 'The dish price does not match the expected response'
    assert (
        dish['id'] == saved_data['dish']['id']
    ), 'The dish ID does not match the expected response'


async def test_delete_dish(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на удаление текущего блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await ac.delete(
        url=reverse(
            delete_dish,
            menu_id=menu['id'],
            submenu_id=submenu['id'],
            dish_id=dish['id'],
        ),
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert (
        response.json()['message'] == 'The dish has been deleted'
    ), 'The deletion message does not match the expected on'


async def test_full_list_menus_after_delete_dish(
    menu_post: dict[str, str],
    submenu_post: dict[str, str],
    dish_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """
    Проверка вывода всех меню со всеми связанными подменю и блюдами.
    """
    response = await ac.get(url=reverse(show_full_list_menus))
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'

    data = response.json()

    assert len(data) == 1, 'There is more than one menu in the response'
    assert (
        data[0]['title'] == menu_post['title']
    ), 'The menu title does not match the expected response'
    assert (
        data[0]['description'] == menu_post['description']
    ), 'The menu description does not match the expected response'
    assert (
        data[0]['id'] == saved_data['menu']['id']
    ), 'The menu ID does not match the expected response'
    assert (
        len(data[0]['submenus']) == 1
    ), 'The submenus count does not match the expected response'

    submenu = data[0]['submenus'][0]

    assert (
        submenu['title'] == submenu_post['title']
    ), 'The submenu title does not match the expected response'
    assert (
        submenu['description'] == submenu_post['description']
    ), 'The submenu description does not match the expected response'
    assert (
        submenu['id'] == saved_data['submenu']['id']
    ), 'The submenu ID does not match the expected response'
    assert (
        len(submenu['dishes']) == 0
    ), 'The dishes count does not match the expected response'


async def test_delete_submenu(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на удаление текущего подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response: Response = await ac.delete(
        url=reverse(delete_submenu, menu_id=menu['id'], submenu_id=submenu['id'])
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert (
        response.json()['message'] == 'The submenu has been deleted'
    ), 'The deletion message does not match the expected on'


async def test_full_list_menus_after_delete_submenu(
    menu_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """
    Проверка вывода всех меню со всеми связанными подменю и блюдами.
    """
    response = await ac.get(url=reverse(show_full_list_menus))
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'

    data = response.json()

    assert len(data) == 1, 'There is more than one menu in the response'
    assert (
        data[0]['title'] == menu_post['title']
    ), 'The menu title does not match the expected response'
    assert (
        data[0]['description'] == menu_post['description']
    ), 'The menu description does not match the expected response'
    assert (
        data[0]['id'] == saved_data['menu']['id']
    ), 'The menu ID does not match the expected response'
    assert (
        len(data[0]['submenus']) == 0
    ), 'The submenus count does not match the expected response'


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


async def test_full_list_menus_after_delete_menu(
    menu_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """
    Проверка вывода всех меню со всеми связанными подменю и блюдами.
    """
    response = await ac.get(url=reverse(show_full_list_menus))
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'

    assert response.json() == [], 'There is a non-empty list in the response'
