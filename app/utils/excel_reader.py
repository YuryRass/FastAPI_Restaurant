import pickle

from app.database.sync_redis import redis_cacher
from app.google_api.spreadsheets import SpreadSheets
from app.utils.json_shemas import JsonDish, JsonMenu, JsonSubmenu


class ExcelReader:
    """Чтение данных из удаленного Excel файла."""

    def __init__(self) -> None:
        self.ss = SpreadSheets()
        self.menus_schema: list[JsonMenu] = []

    def get_menus(self) -> list[JsonMenu]:
        """Возвращает заполненную json структуру меню ресторана."""
        self.__reader()
        return self.menus_schema

    def __reader(self) -> None:
        """
        Считывает данные всех меню ресторана из удаленного
        excel файла и сохраняет их в json структуре.
        """
        remote_data = self.ss.get_values()
        if remote_data is None:
            return
        for row in remote_data:
            # Меню
            if row[0]:
                self.menus_schema.append(
                    JsonMenu(
                        id=row[0],
                        title=row[1],
                        description=row[2],
                        submenus=[],
                    )
                )
            # Подменю
            elif row[1]:
                self.menus_schema[-1].submenus.append(
                    JsonSubmenu(
                        id=row[1],
                        title=row[2],
                        description=row[3],
                        dishes=[],
                    )
                )
            # Блюда
            else:  # row[2] != ''
                # получаем скидку на блюдо
                discount = None
                if len(row) == 7:
                    discount = self.__get_discount(row[6])
                if discount:
                    new_price = (
                        float(row[5].replace(',', '.')) * (1 - discount / 100)
                        if discount
                        else float(row[5].replace(',', '.'))
                    )
                    # Добавляем в кеш новую цену
                    if redis_cacher.get(row[2]):
                        redis_cacher.delete(row[2])
                    redis_cacher.set(row[2], pickle.dumps(new_price))

                self.menus_schema[-1].submenus[-1].dishes.append(
                    JsonDish(
                        id=row[2],
                        title=row[3],
                        description=row[4],
                        price=round(float(row[5].replace(',', '.')), 2),
                    )
                )

    def __get_discount(self, discount: str | None) -> int | None:
        """Проверка и получение скидки на блюдо."""
        if discount and discount.isdigit() and 0 <= int(discount) <= 100:
            return int(discount)
        return None
