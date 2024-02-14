import logging

from celery import shared_task

from app.tasks.db_updater import DBUpdater
from app.utils.excel_reader import ExcelReader

er = ExcelReader()


@shared_task(bind=True, name='task')
async def update_db() -> None:
    """Обновление данных в БД из удаленного excel файла."""
    try:
        menus_schema = er.get_menus()
        updater = DBUpdater(menus_schema)
        return await updater.run_update_db()
    except Exception as exc:
        logging.error(exc)
