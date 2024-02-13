import asyncio
import logging

from app.tasks.celery import celery
from app.tasks.db_updater import DBUpdater
from app.utils.excel_reader import ExcelReader

er = ExcelReader()
loop = asyncio.get_event_loop()


async def update():
    menus_schema = er.get_menus()
    updater = DBUpdater(menus_schema)
    await updater.run()


@celery.task
def update_db() -> None:
    """Обновление данных в БД из удаленного excel файла."""
    try:
        return loop.run_until_complete(update())
    except Exception as exc:
        logging.error(exc)
