# from app.tasks.celery import celery
from app.tasks.db_updater import DBUpdater

# from app.tasks.excel_writer import ExcelWorker
from app.utils.excel_reader import ExcelReader


# @celery.task
def update_db() -> None:
    """Обновление данных в БД из excel файла."""
    try:
        print('Запуск задачи обновления БД')
        er = ExcelReader()
        menus_schema = er.get_menus()
        updater = DBUpdater(menus_schema)
        updater.run()
    except Exception as error:
        print(f'Ошибка при обновлении БД: {error}')

# @celery.task
# def write_excel() -> None:
#     """Запись данных в локальный excel файл."""
#     try:
#         print('Запуск задачи записи в Excel')
#         ew = ExcelWorker()
#         ew.write_data()
#     except Exception as error:
#         print(f'Ошибка при записи в Excel: {error}')
