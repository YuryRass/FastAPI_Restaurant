from app.config import settings
from celery import Celery


# celery --app=app.tasks.celery:celery worker -l INFO
celery = Celery(
    "tasks",
    broker=settings.RABITMQ_URL,
    include=["app.tasks.tasks"],
)
