import logging
from config import settings
from tasks.celery_app import celery_app

logger = logging.getLogger(__name__)

@celery_app.task(name="backend.tasks.email_tasks.send_email_task")
def send_email_task(to_email: str, email_type: str, context: dict):
    logger.info(f"Mock sending {email_type} to {to_email}")
