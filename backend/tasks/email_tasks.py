import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from backend.tasks.celery_app import celery_app
from backend.config import settings

logger = logging.getLogger(__name__)

# Map template names to SendGrid template IDs (or subjects for dev mode fallback)
TEMPLATE_SUBJECTS = {
    "welcome": "Welcome to AI Productivity OS!",
    "audit_complete": "Your AI Optimization Audit is Complete",
    "invite": "You have been invited to join an organization"
}

@celery_app.task(name="backend.tasks.email_tasks.send_email_task")
def send_email_task(to_email: str, template: str, context: dict):
    subject = TEMPLATE_SUBJECTS.get(template, "Notification from AI Productivity OS")

    sendgrid_api_key = getattr(settings, "SENDGRID_API_KEY", None)

    if sendgrid_api_key:
        try:
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com")
            message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=subject,
                html_content=f"<p>Template: {template}</p><p>Context: {context}</p>"
            )

            # If using actual SendGrid dynamic templates:
            # message.template_id = "d-your-template-id"
            # message.dynamic_template_data = context

            sg = SendGridAPIClient(sendgrid_api_key)
            response = sg.send(message)
            return {"status": "sent", "status_code": response.status_code}
        except Exception as e:
            logger.error(f"Failed to send email via SendGrid: {str(e)}")
            raise e
    else:
        # Dev mode: Log email to console
        logger.info(f"--- EMAIL LOG (DEV MODE) ---")
        logger.info(f"To: {to_email}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Template: {template}")
        logger.info(f"Context: {context}")
        logger.info(f"----------------------------")
        return {"status": "logged", "message": "Email logged to console (SendGrid API key not set)"}
