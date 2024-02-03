from typing import TypeVar
from app.dish.model import Dish
from app.menu.model import Menu
from app.submenu.model import Submenu

ModelType = TypeVar('ModelType', Dish, Menu, Submenu)
