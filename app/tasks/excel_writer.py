from openpyxl import Workbook

from app.config import settings
from app.google_api.spreadsheets import SpreedSheets


class ExcelWorker:
    def __init__(self) -> None:
        self.excel_file = settings.EXCEL_PATH
        self.ss = SpreedSheets()
        self.wb = Workbook()
        self.ws = self.wb.active  # worksheet object.

    def write_data(self) -> None:
        """Запись данных из удаленной excel таблицы в локальную."""
        data_list = self.ss.get_values()
        for row in data_list:
            self.ws.append(row)
        self.wb.save(self.excel_file)
