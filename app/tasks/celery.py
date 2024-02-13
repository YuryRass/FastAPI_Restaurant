from datetime import timedelta

from celery import Celery

from app.config import settings

celery = Celery(
    'tasks',
    broker=settings.RABITMQ_URL,
    include=['app.tasks.tasks'],
)


celery.conf.beat_schedule = {
    'update_db_every_15_seconds': {
        'task': 'app.tasks.tasks.update_db',
        'schedule': timedelta(seconds=15),
    },
}
