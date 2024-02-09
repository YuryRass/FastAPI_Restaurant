from typing import Any

import httpx
from jsondiff import diff

from app.config import settings
from app.menu.model import Menu
from app.utils.json_shemas import JsonMenu


class DBUpdater:
    """Обновление данных в БД после чтения excel файла."""

    def __init__(self, excel_data: list[JsonMenu]):
        self.excel_data = excel_data
        self.db_data: Any = self.__get_menus_full_list_from_db()

    def get_diff(self):
        print(self.db_data)
        print('\n\n')
        return diff(self.db_data, self.excel_data)

    def __get_menus_full_list_from_db(self) -> Any:
        """Получене полного списка всех меню."""
        r = httpx.get(f'{settings.APP_LINK}{Menu.FULL_LINK}')
        return r.json()
