from celery import Celery
from app.config import settings


# in terminal: celery -A app.tasks.celery_root:celery worker --loglevel=INFO
celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=["app.tasks.tasks"]
)
