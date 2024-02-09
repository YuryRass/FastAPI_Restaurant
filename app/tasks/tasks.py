from app.tasks.celery import celery
from app.utils.excel_reader import ExcelReader
from app.tasks.db_updater import DBUpdater


@celery.task(
    default_retry_delay=15,
    max_retries=None,
)
def update_db():
    """Обновление данных в БД из excel файла."""
    try:
        er = ExcelReader()
        menus = er.get_menus()
        updater = DBUpdater(menus)
        updater.get_diff()
        # update_base.delay()
    except Exception as error:
        print(error)
    finally:
        update_db.retry()
