from app.tasks.celery import celery
from app.tasks.db_updater import DBUpdater
from app.tasks.excel_writer import ExcelWorker
from app.utils.excel_reader import ExcelReader


@celery.task(
    default_retry_delay=15,
    max_retries=None,
)
def update_db() -> None:
    """Обновление данных в БД из excel файла."""
    try:
        er = ExcelReader()
        menus = er.get_menus()
        updater = DBUpdater(menus)
        updater.get_diff()
    except Exception as error:
        print(error)
    finally:
        update_db.retry()


@celery.task(
    default_retry_delay=15,
    max_retries=None,
)
def write_excel() -> None:
    """Запись данных в локальный excel файл."""
    try:
        ew = ExcelWorker()
        ew.write_data()
    except Exception as error:
        print(error)
    finally:
        write_excel.retry()
