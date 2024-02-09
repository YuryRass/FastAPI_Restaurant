from celery import Celery

from app.config import settings

# celery --app=app.tasks.celery:celery worker -l INFO
celery = Celery(
    'tasks',
    broker=settings.RABITMQ_URL,
    include=['app.tasks.tasks'],
)
