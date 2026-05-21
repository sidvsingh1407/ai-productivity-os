import os
from celery import Celery
from backend.config import settings

# To start worker: celery -A backend.tasks.celery_app worker --loglevel=info

redis_url = getattr(settings, "REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "ai_productivity_os",
    broker=redis_url,
    backend=redis_url,
    include=["backend.tasks.pdf_tasks", "backend.tasks.email_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    result_expires=3600,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    broker_connection_retry_on_startup=True,
    task_default_retry_delay=60,
    task_publish_retry=True,
)

# Optional max retries config if explicitly set
# Tasks can also define max_retries natively using @celery_app.task(max_retries=3)
