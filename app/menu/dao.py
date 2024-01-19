from dao.base import BaseDAO
from app.menu.model import Menu

# {
#     "id": "9a5bce5f-4462-4d12-a66c-d59584b19ee8",
#     "title": "My menu 1",
#     "description": "My menu description 1",
#     "submenus_count": 0,
#     "dishes_count": 0
# }


class SubmenuDAO(BaseDAO):
    model = Menu
