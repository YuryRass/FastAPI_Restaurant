
import requests

from typing import Any
from app.utils.json_shemas import JsonMenu
from app.menu.model import Menu

class DBUpdater:
    """Обновление данных в БД после чтения excel файла."""

    def __init__(self, excel_data: list[JsonMenu]):
        self.excel_data = excel_data

    def get_menus_full_list_from_db(seld):
        response = requests.get(url=Menu.FULL_LINK).json()
        return response
