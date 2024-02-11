from openpyxl import Workbook

from app.config import settings
from app.google_api.spreadsheets import SpreadSheets


class ExcelWorker:
    def __init__(self) -> None:
        self.excel_file = settings.EXCEL_PATH
        self.ss = SpreadSheets()
        self.wb = Workbook()
        self.ws = self.wb.active  # worksheet object.

    def write_data(self) -> None:
        """Запись данных из удаленной excel таблицы в локальную."""
        remote_data = self.ss.get_values()
        if remote_data is None:
            return
        for row in remote_data:
            self.ws.append(row)
        self.wb.save(self.excel_file)
