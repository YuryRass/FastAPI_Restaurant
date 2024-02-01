import uuid

from fastapi import APIRouter, Response, status
from sqlalchemy.exc import IntegrityError

from app.exceptions import MenuNotFoundException, SimilarMenuTitlesException
from app.menu.dao import MenuDAO
from app.menu.shemas import OutSMenu, SMenu

router: APIRouter = APIRouter(
    prefix='/menus',
    tags=['Menus'],
)


@router.post('')
async def add_menu(menu: SMenu, responce: Response) -> OutSMenu:
    try:
        menu_res = await MenuDAO.add(
            title=menu.title,
            description=menu.description,
        )
    except IntegrityError:
        raise SimilarMenuTitlesException

    responce.status_code = status.HTTP_201_CREATED
    added_menu = await MenuDAO.show(menu_res['id'])
    return added_menu


@router.get('')
async def show_menus() -> list[OutSMenu]:
    menus = await MenuDAO.show()

    return menus


@router.get('/{menu_id}')
async def show_menu_by_id(menu_id: uuid.UUID) -> OutSMenu:
    menu = await MenuDAO.show(menu_id)
    if not menu:
        raise MenuNotFoundException

    return menu


@router.patch('/{menu_id}')
async def update_menu(menu_id: uuid.UUID, new_data: SMenu) -> OutSMenu:
    menu = await MenuDAO.show(menu_id)
    if not menu:
        raise MenuNotFoundException

    updated_menu = await MenuDAO.update(
        menu_id,
        title=new_data.title,
        description=new_data.description,
    )

    menu_res = await MenuDAO.show(updated_menu['id'])

    return menu_res


@router.delete('/{menu_id}')
async def delete_menu(menu_id: uuid.UUID) -> dict[str, bool | str]:
    menu = await MenuDAO.delete_record(id=menu_id)
    if menu:
        return {'status': True, 'message': 'The menu has been deleted'}
