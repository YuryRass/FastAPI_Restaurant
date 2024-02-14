import asyncio
import functools
import logging

from app.tasks.celery import celery

from app.tasks.db_updater import DBUpdater
from app.utils.excel_reader import ExcelReader


def sync(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.get_event_loop().run_until_complete(f(*args, **kwargs))
    return wrapper

@celery.task
@sync
async def update_db() -> None:
    """Обновление данных в БД из удаленного excel файла."""
    try:
        er = ExcelReader()
        menus_schema = er.get_menus()
        updater = DBUpdater(menus_schema)
        return await updater.run_update_db()
    except Exception as exc:
        logging.error(exc)
