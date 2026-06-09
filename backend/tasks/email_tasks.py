import os
import logging
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from tasks.celery_app import celery_app
from config import settings

logger = logging.getLogger(__name__)

from jinja2 import Environment, FileSystemLoader, select_autoescape

# Initialize Jinja2 environment for HTML templates
template_env = Environment(
    loader=FileSystemLoader(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'emails')),
    autoescape=select_autoescape(['html', 'xml'])
)

# Map template names to SendGrid template IDs (or subjects for dev mode fallback)
TEMPLATE_SUBJECTS = {
    "welcome": "Welcome to AI Productivity OS!",
    "audit_complete": "Your AI Optimization Audit is Complete",
    "invite": "You have been invited to join an organization",
    "verify_email": "Verify Your Email Address",
    "password_reset": "Password Reset Request"
}

def render_template(template_name: str, context: dict) -> str:
    try:
        template = template_env.get_template(f"{template_name}.html")
        return template.render(**context)
    except Exception as e:
        logger.error(f"Failed to render template {template_name}: {e}")
        return f"<p>Template: {template_name}</p><p>Context: {context}</p>"

@celery_app.task(name="backend.tasks.email_tasks.send_email_task")
def send_email_task(to_email: str, template: str, context: dict):
    subject = TEMPLATE_SUBJECTS.get(template, "Notification from AI Productivity OS")
    html_content = render_template(template, context)

    sendgrid_api_key = getattr(settings, "SENDGRID_API_KEY", None)

    if sendgrid_api_key:
        try:
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@example.com")
            message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=subject,
                html_content=html_content
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
