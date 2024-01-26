from http import HTTPStatus
from typing import Any
from httpx import AsyncClient, Response


async def test_add_menu(
    menu_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка добавления нового меню"""

    response: Response = await ac.post(
        url="/menus",
        json=menu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, "The response status is not 201"
    assert "id" in response.json(), "The menu ID is not in the response"
    assert "title" in response.json(), "The menu title is not in the response"
    assert (
        "description" in response.json()
    ), "The menu description is not in the response"
    assert (
        "submenus_count" in response.json()
    ), "The submenus_count is not in the response"
    assert "dishes_count" in response.json(), "The dishes_count is not in the response"
    assert (
        response.json()["title"] == menu_post["title"]
    ), "The menu title does not match the expected response"
    assert (
        response.json()["description"] == menu_post["description"]
    ), "The menu description does not match the expected response"

    saved_data["menu"] = response.json()


async def test_submenu_empty(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка получения пустого списка подменю"""
    menu = saved_data["menu"]
    response: Response = await ac.get(url=f"/menus/{menu['id']}/submenus")
    assert response.status_code == HTTPStatus.OK, "The response status is not 200"
    assert response.json() == [], "There is a non-empty list in the response"


async def test_add_submenu(
    submenu_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на добавление нового подменю"""

    menu = saved_data["menu"]
    response: Response = await ac.post(
        url=f"/menus/{menu['id']}/submenus",
        json=submenu_post,
    )
    assert response.status_code == HTTPStatus.CREATED, "The response status is not 201"
    assert "id" in response.json(), "The submenu ID is not in the response"
    assert "title" in response.json(), "The submenu title is not in the response"
    assert (
        "description" in response.json()
    ), "The submenu description is not in the response"

    assert "dishes_count" in response.json(), "The dishes_count is not in the response"
    assert (
        response.json()["title"] == submenu_post["title"]
    ), "The submenu title does not match the expected response"
    assert (
        response.json()["description"] == submenu_post["description"]
    ), "The submenu description does not match the expected response"

    saved_data["submenu"] = response.json()


async def test_add_submenu_similar(
    submenu_post: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на добавление нового подменю с одинаковым названием"""

    menu = saved_data["menu"]
    response: Response = await ac.post(
        url=f"/menus/{menu['id']}/submenus",
        json=submenu_post,
    )
    assert (
        response.status_code == HTTPStatus.BAD_REQUEST
    ), "The response status is not 400"


async def test_submenus_not_empty(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на получение непустого списка подменю"""

    menu = saved_data["menu"]
    response: Response = await ac.get(url=f"/menus/{menu['id']}/submenus")
    assert response.status_code == HTTPStatus.OK, "The response status is not 200"
    assert response.json() != [], "There is an empty list in the response"


async def test_get_submenu_by_id(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Получение созданного подменю по его ID"""

    menu = saved_data["menu"]
    submenu = saved_data["submenu"]
    response: Response = await ac.get(
        url=f"/menus/{menu['id']}/submenus/{submenu['id']}",
    )
    assert response.status_code == HTTPStatus.OK, "The response status is not 200"
    assert (
        response.json()["id"] == submenu["id"]
    ), "The submenu ID does not match the expected response"
    assert (
        response.json()["title"] == submenu["title"]
    ), "The submenu title does not match the expected response"
    assert (
        response.json()["description"] == submenu["description"]
    ), "The submenu description does not match the expected response"
    assert (
        response.json()["dishes_count"] == 0
    ), "The dishes_count does not match the expected response"


async def test_update_submenu(
    submenu_patch: dict[str, str],
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на изменение текущего подменю"""

    menu = saved_data["menu"]
    submenu = saved_data["submenu"]
    response: Response = await ac.patch(
        url=f"/menus/{menu['id']}/submenus/{submenu['id']}",
        json=submenu_patch,
    )
    assert response.status_code == HTTPStatus.OK, "The response status is not 200"

    assert (
        response.json()["title"] == submenu_patch["title"]
    ), "The submenu title does not match the expected response"
    assert (
        response.json()["description"] == submenu_patch["description"]
    ), "The submenu description does not match the expected response"

    saved_data["submenu"] = response.json()


async def test_get_updated_submenu_by_id(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на получение измененного подменю"""

    menu = saved_data["menu"]
    submenu = saved_data["submenu"]
    response: Response = await ac.get(
        url=f"/menus/{menu['id']}/submenus/{submenu['id']}",
    )
    assert response.status_code == HTTPStatus.OK, "The response status is not 200"
    assert (
        response.json()["id"] == submenu["id"]
    ), "The submenu ID does not match the expected response"
    assert (
        response.json()["title"] == submenu["title"]
    ), "The submenu title does not match the expected response"
    assert (
        response.json()["description"] == submenu["description"]
    ), "The submenu description does not match the expected response"
    assert (
        response.json()["dishes_count"] == 0
    ), "The dishes_count does not match the expected response"


async def test_delete_submenu(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на удаление текущего подменю"""

    menu = saved_data["menu"]
    submenu = saved_data["submenu"]
    response: Response = await ac.delete(
        url=f"/menus/{menu['id']}/submenus/{submenu['id']}"
    )
    assert response.status_code == HTTPStatus.OK, "The response status is not 200"
    assert (
        response.json()["message"] == "The submenu has been deleted"
    ), "The deletion message does not match the expected on"


async def test_submenu_empty_after_delete(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на получение пустого списка подменю после удаления"""

    menu = saved_data["menu"]
    response = await ac.get(
        url=f"/menus/{menu['id']}/submenus",
    )
    assert response.status_code == HTTPStatus.OK, "The response status is not 200"
    assert response.json() == [], "There is a non-empty list in the response"


async def test_get_deleted_submenu(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на отсутствие удаленного подменю"""

    menu = saved_data["menu"]
    submenu = saved_data["submenu"]
    response = await ac.get(
        url=f"/menus/{menu['id']}/submenus/{submenu['id']}",
    )
    assert (
        response.status_code == HTTPStatus.NOT_FOUND
    ), "The response status is not 404"
    assert (
        response.json()["detail"] == "submenu not found"
    ), "The deletion message does not match the expected on"


async def test_delete_menu(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на удаление текущего меню"""

    menu = saved_data["menu"]
    response: Response = await ac.delete(
        url=f"/menus/{menu['id']}",
    )
    assert response.status_code == HTTPStatus.OK, "The response status is not 200"
    assert (
        response.json()["message"] == "The menu has been deleted"
    ), "The deletion message does not match the expected on"


async def test_get_menu_after_delete(
    saved_data: dict[str, Any],
    ac: AsyncClient,
) -> None:
    """Проверка на отсутствие удаленного меню"""

    menu = saved_data["menu"]
    response = await ac.get(url=f"/menus/{menu['id']}")
    assert (
        response.status_code == HTTPStatus.NOT_FOUND
    ), "The response status is not 404"
    assert (
        response.json()["detail"] == "menu not found"
    ), "The deletion message does not match the expected on"


# async def test_post_objects_for_cascade_check(
#     menu_post: dict[str, str],
#     submenu_post: dict[str, str],
#     saved_data: dict[str, Any],
#     client: AsyncClient,
# ) -> None:
#     """Добавление нового меню и подменю для последующей проверки
#     каскадного удаления."""
#     response = await client.post(
#         reverse(post_new_menu),
#         json=menu_post,
#     )
#     assert response.status_code == HTTPStatus.CREATED, \
#         'Статус ответа не 201'

#     saved_data['menu'] = response.json()

#     menu = saved_data['menu']
#     response = await client.post(
#         reverse(post_new_submenu, menu_id=menu['id']),
#         json=submenu_post,
#     )
#     assert response.status_code == HTTPStatus.CREATED, \
#         'Статус ответа не 201'

#     saved_data['submenu'] = response.json()


# async def test_delete_menu_for_cascade_check(
#     saved_data: dict[str, Any],
#     client: AsyncClient,
# ) -> None:
#     """Удаление текущего меню."""
#     menu = saved_data['menu']
#     response = await client.delete(
#         reverse(destroy_menu, menu_id=menu['id']),
#     )
#     assert response.status_code == HTTPStatus.OK, \
#         'Статус ответа не 200'
#     assert response.text == '"menu deleted"', \
#         'Сообщение об удалении не соответствует ожидаемому'


# async def test_get_deleted_submenu_cascade_check(
#     saved_data: dict[str, Any],
#     client: AsyncClient,
# ) -> None:
#     """Получение подменю удаленного меню, проверка каскадного удаления."""
#     menu = saved_data['menu']
#     submenu = saved_data['submenu']
#     response = await client.get(
#         reverse(get_submenu, menu_id=menu['id'], submenu_id=submenu['id']),
#     )
#     assert response.status_code == HTTPStatus.NOT_FOUND, \
#         'Статус ответа не 404'
#     assert response.json()['detail'] == 'submenu not found', \
#         'Сообщение об ошибке не соответствует ожидаемому'
