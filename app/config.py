from typing import Literal

from pydantic import EmailStr, FilePath, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройка приложения."""

    MODE: Literal['DEV', 'TEST']
    CELERY_RUN: bool

    # данные для базы данных PostgreSQL
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    # данные для тестовой базы данных PostgreSQL
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    # данные для Redis
    REDIS_HOST: str
    REDIS_PORT: int

    # Время жизни записи в Redis
    EXPIRATION: int = 600

    # Excel файл с данными о меню
    EXCEL_PATH: FilePath = 'app/admin/Menu.xlsx'

    APP_LINK: HttpUrl

    RABBITMQ_DEFAULT_USER: str
    RABBITMQ_DEFAULT_PASS: str
    RABBITMQ_DEFAULT_PORT: int
    RABBITMQ_HOST: str

    # Google Sheets API
    API_CREDENTIALS_FILE: FilePath
    EMAIL: EmailStr
    SHEET_ID: str

    @property
    def DATABASE_URL(self) -> str:
        """URL адрес базы данных."""
        return (
            f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@'
            f'{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'
        )

    @property
    def TEST_DATABASE_URL(self) -> str:
        """URL адрес тестовой базы данных."""
        return (
            f'postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASS}@'
            f'{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}'
        )

    @property
    def REDIS_URL(self) -> str:
        """URL адрес Redis."""
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    @property
    def RABITMQ_URL(self) -> str:
        """URL адрес брокера сообщений RabbitMQ."""
        return (
            f'amqp://{self.RABBITMQ_DEFAULT_USER}:{self.RABBITMQ_DEFAULT_PASS}'
            f'@{self.RABBITMQ_HOST}:{self.RABBITMQ_DEFAULT_PORT}'
        )

    @property
    def SCOPES(self) -> list[str]:
        """Права доступа к API"""
        return [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
        ]

    model_config = SettingsConfigDict(env_file='.env')


settings: Settings = Settings()
