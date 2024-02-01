from typing import Sequence, TypeAlias

from sqlalchemy.engine.row import RowMapping

from app.menu.model import Menu
from app.submenu.model import Submenu
from app.dish.model import Dish


ModelType: TypeAlias = Menu | Submenu | Dish | None

MappingOut: TypeAlias = Sequence[RowMapping] | RowMapping | None
