from http import HTTPStatus
from typing import Any

from httpx import AsyncClient, Response

from app.dish.router import (
    add_dish,
    delete_dish,
    show_dish_by_id,
    show_dishes,
    update_dish,
)
from app.menu.router import add_menu, delete_menu
from app.submenu.router import add_submenu, delete_submenu
from app.utils.url import reverse


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


async def test_dish_empty(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка получения пустого списка блюд."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await ac.get(
        url=reverse(show_dishes, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert response.json() == [], 'There is an empty list in the response'


async def test_add_dish(
    dish_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на добавление нового блюда."""
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


async def test_add_dish_similar(
    dish_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на добавление нового блюда с одинаковым названием."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await ac.post(
        url=reverse(add_dish, menu_id=menu['id'], submenu_id=submenu['id']),
        json=dish_post,
    )
    assert (
        response.status_code == HTTPStatus.BAD_REQUEST
    ), 'The response status is not 400'


async def test_dishes_not_empty(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на получение непустого списка блюд."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await ac.get(
        url=reverse(show_dishes, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert response.json() != [], 'There is an empty list in the response'


async def test_get_posted_dish(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на получение созданного блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await ac.get(
        url=reverse(
            show_dish_by_id,
            menu_id=menu['id'],
            submenu_id=submenu['id'],
            dish_id=dish['id'],
        ),
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert (
        response.json()['id'] == dish['id']
    ), 'The dish ID does not match the expected response'
    assert (
        response.json()['title'] == dish['title']
    ), 'The dish title does not match the expected response'
    assert (
        response.json()['description'] == dish['description']
    ), 'The dish description does not match the expected response'
    assert (
        response.json()['price'] == dish['price']
    ), 'The dish price does not match the expected response'


async def test_update_dish(
    dish_patch: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на изменение текущего блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await ac.patch(
        url=reverse(
            update_dish,
            menu_id=menu['id'],
            submenu_id=submenu['id'],
            dish_id=dish['id'],
        ),
        json=dish_patch,
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert 'id' in response.json(), 'The dish ID is not in the response'
    assert 'title' in response.json(), 'The dish title is not in the response'
    assert (
        'description' in response.json()
    ), 'The dish description is not in the response'
    assert 'price' in response.json(), 'The dish price is not in the response'

    assert (
        response.json()['title'] == dish_patch['title']
    ), 'The dish title does not match the expected response'
    assert (
        response.json()['description'] == dish_patch['description']
    ), 'The dish description does not match the expected response'
    assert response.json()['price'] == '654.12'

    saved_data['dish'] = response.json()


async def test_get_updated_dish(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на получение обновленного блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await ac.get(
        url=reverse(
            show_dish_by_id,
            menu_id=menu['id'],
            submenu_id=submenu['id'],
            dish_id=dish['id'],
        ),
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert (
        response.json()['id'] == dish['id']
    ), 'The dish ID does not match the expected response'
    assert (
        response.json()['title'] == dish['title']
    ), 'The dish title does not match the expected response'
    assert (
        response.json()['description'] == dish['description']
    ), 'The dish description does not match the expected response'
    assert (
        response.json()['price'] == dish['price']
    ), 'The dish price does not match the expected response'


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


async def test_dishes_empty_after_delete(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка получения пустого списка блюд после удаления."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await ac.get(
        url=reverse(
            show_dishes,
            menu_id=menu['id'],
            submenu_id=submenu['id'],
        ),
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert response.json() == [], 'There is a non-empty list in the response'


async def test_get_deleted_dish(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на получение удаленного блюда."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await ac.get(
        url=reverse(
            show_dish_by_id,
            menu_id=menu['id'],
            submenu_id=submenu['id'],
            dish_id=dish['id'],
        ),
    )
    assert (
        response.status_code == HTTPStatus.NOT_FOUND
    ), 'The response status is not 200'
    assert (
        response.json()['detail'] == 'dish not found'
    ), 'The error message does not match the expected on'


async def test_delete_submenu(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на удаление текущего подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await ac.delete(
        url=reverse(delete_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert (
        response.json()['message'] == 'The submenu has been deleted'
    ), 'The deletion message does not match the expected response'


async def test_deleted_submenu_dishes_empty(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на получение пустого списка блюд у несуществующего подменю."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await ac.get(
        url=reverse(show_dishes, menu_id=menu['id'], submenu_id=submenu['id']),
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert response.json() == [], 'There is a non-empty list in the response'


async def test_post_for_cascade_deletion(
    submenu_post: dict[str, str],
    dish_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Добавление нового подменю и блюда для проверки каскадного удаления."""
    menu = saved_data['menu']
    response = await ac.post(
        url=reverse(add_submenu, menu_id=menu['id']),
        json=submenu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, 'The response status is not 201'

    saved_data['submenu'] = response.json()

    submenu = saved_data['submenu']
    response = await ac.post(
        url=reverse(add_dish, menu_id=menu['id'], submenu_id=submenu['id']),
        json=dish_post,
    )
    assert response.status_code == HTTPStatus.CREATED, 'The response status is not 201'

    saved_data['dish'] = response.json()


async def test_delete_submenu_for_cascade_check(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Удаление текущего подменю для проверки каскадного удаления."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    response = await ac.delete(
        url=reverse(
            delete_submenu,
            menu_id=menu['id'],
            submenu_id=submenu['id'],
        )
    )
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert (
        response.json()['message'] == 'The submenu has been deleted'
    ), 'The deletion message does not match the expected response'


async def test_get_deleted_dish_for_cascade_check(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Получение удаленного блюда (проверка каскадного удаления)."""
    menu = saved_data['menu']
    submenu = saved_data['submenu']
    dish = saved_data['dish']
    response = await ac.get(
        url=reverse(
            show_dish_by_id,
            menu_id=menu['id'],
            submenu_id=submenu['id'],
            dish_id=dish['id'],
        ),
    )
    assert (
        response.status_code == HTTPStatus.NOT_FOUND
    ), 'The response status is not 404'
    assert (
        response.json()['detail'] == 'dish not found'
    ), 'The error message does not match the expected response'


async def test_delete_menu_finally(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Удаление текущего меню."""
    menu = saved_data['menu']
    response = await ac.delete(url=reverse(delete_menu, menu_id=menu['id']))
    assert response.status_code == HTTPStatus.OK, 'The response status is not 200'
    assert (
        response.json()['message'] == 'The menu has been deleted'
    ), 'The error message does not match the expected response'
