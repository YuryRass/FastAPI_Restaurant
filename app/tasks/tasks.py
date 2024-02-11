import logging

from app.tasks.celery import celery
from app.tasks.db_updater import DBUpdater
from app.utils.excel_reader import ExcelReader


@celery.task
def update_db() -> None:
    """Обновление данных в БД из удаленного excel файла."""
    try:
        er = ExcelReader()
        menus_schema = er.get_menus()
        updater = DBUpdater(menus_schema)
        updater.run()
    except Exception as e:
        logging.error(e)
