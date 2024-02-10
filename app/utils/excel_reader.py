from app.google_api.spreadsheets import SpreedSheets
from app.utils.json_shemas import JsonDish, JsonMenu, JsonSubmenu


class ExcelReader:
    """Чтение данных из удаленного Excel файла."""

    def __init__(self) -> None:
        self.ss = SpreedSheets()
        self.menus_schema: list[JsonMenu] = []

    def get_menus(self) -> list[JsonMenu]:
        """Возвращает заполненную json структуру меню ресторана."""
        self.__reader()
        return self.menus_schema

    def __reader(self) -> None:
        """
        Считывает данные всех меню ресторана из удаленного
        excel файла и сохраняет их в json структуре..
        """
        list_data = self.ss.get_values()
        for row in list_data:
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

                self.menus_schema[-1].submenus[-1].dishes.append(
                    JsonDish(
                        id=row[2],
                        title=row[3],
                        description=row[4],
                        price=(
                            float(row[5].replace(',', '.')) * discount
                            if discount
                            else float(row[5].replace(',', '.'))
                        ),
                    )
                )
        # print('self.menus', self.menus_json)
        # print('menus', self.menus_schema)

    def __get_discount(self, discount: str | None) -> int | None:
        """Проверка и получение скидки на блюдо."""
        if discount and discount.isdigit() and 0 <= int(discount) <= 100:
            return int(discount)
        return None
