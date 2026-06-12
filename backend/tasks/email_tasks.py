import logging
from config import settings

logger = logging.getLogger(__name__)

def send_email_task(to_email: str, email_type: str, context: dict):
    logger.info(f"Mock sending {email_type} to {to_email}")
