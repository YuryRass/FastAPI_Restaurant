from typing import Any

from google.oauth2.service_account import Credentials
from googleapiclient import discovery

from app.config import settings


class SpreadSheets:
    """Работа с Google Sheets API."""

    def __init__(self) -> None:
        self.service, self.credentials = self.__auth()

    def get_values(self) -> list[list[str]] | None:
        """Получение данных таблицы из Google Sheets API."""
        # self.__set_user_permissions() <- используется, если нет прав доступа
        values = self.__spreadsheet_get_values()
        return values

    def create_spreadsheet(self) -> str:
        """
        Создание Google sheet таблицы.
        Используя данную функцию я создавал таблицу в Google Sheets и получал ее ID.
        """
        # Тело spreadsheet
        spreadsheet_body = {
            # Свойства документа
            'properties': {'title': 'Menu', 'locale': 'ru_RU'},
            # Свойства листов документа
            'sheets': [
                {
                    'properties': {
                        'sheetType': 'GRID',
                        'sheetId': 0,
                        'title': 'menu',
                        'gridProperties': {'columnCount': 7},
                    }
                }
            ],
        }

        request = self.service.spreadsheets().create(body=spreadsheet_body)
        response = request.execute()
        spreadsheet_id = response['spreadsheetId']
        print('https://docs.google.com/spreadsheets/d/' + spreadsheet_id)
        self.__set_user_permissions(spreadsheet_id)
        return spreadsheet_id

    def __auth(self) -> tuple[discovery.Resource, Credentials]:
        """Авторизация в Google."""
        # Создаём экземпляр класса Credentials.
        credentials = Credentials.from_service_account_file(
            filename=settings.API_CREDENTIALS_FILE,
            scopes=settings.SCOPES,
        )
        # Создаём экземпляр класса Resource.
        service = discovery.build('sheets', 'v4', credentials=credentials)
        return service, credentials

    def __set_user_permissions(self, sheet_id: str = settings.SHEET_ID) -> None:
        """Установка прав доступа."""
        permissions_body = {
            'type': 'user',  # Тип учетных данных.
            'role': 'writer',  # Права доступа для учётной записи.
            'emailAddress': settings.EMAIL,  # Ваш личный гугл-аккаунт.
        }

        # Создаётся экземпляр класса Resource для Google Drive API.
        drive_service = discovery.build('drive', 'v3', credentials=self.credentials)

        # Формируется и сразу выполняется запрос на выдачу прав вашему аккаунту.
        drive_service.permissions().create(
            fileId=sheet_id, body=permissions_body, fields='id'
        ).execute()

    def __spreadsheet_get_values(self) -> list[list[str]] | None:
        """Возвращение данных таблицы из Google Sheets API."""
        # Формирование запроса к Google Sheets API.
        request = (
            self.service.spreadsheets()
            .values()
            .get(
                spreadsheetId=settings.SHEET_ID,
                range='menu!A1:G',
                majorDimension='ROWS',
            )
        )
        # Выполнение запроса и возвращение данных
        res: dict[str, Any] = request.execute()
        return res.get('values')
