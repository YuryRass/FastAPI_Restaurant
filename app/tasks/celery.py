from datetime import timedelta

from celery import Celery

from app.config import settings

# celery --app=app.tasks.celery:celery worker -l INFO
celery = Celery(
    'tasks',
    broker=settings.RABITMQ_URL,
    include=['app.tasks.tasks'],
)


# Добавьте этот блок в конец файла celery_app.py
celery.conf.beat_schedule = {
    'update_db_every_35_seconds': {
        'task': 'app.tasks.tasks.update_db',
        'schedule': timedelta(seconds=35),
    },
    'write_excel_every_35_seconds': {
        'task': 'app.tasks.tasks.write_excel',
        'schedule': timedelta(seconds=35),
    },
}
