import httpx
import os
import logging
from jinja2 import Environment, FileSystemLoader, select_autoescape

logger = logging.getLogger(__name__)

# Setup Jinja2 environment for email templates
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'templates', 'emails')
env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=select_autoescape(['html', 'xml'])
)

def render_email_template(template_name: str, context: dict) -> str:
    """Renders an email template with the given context."""
    try:
        template = env.get_template(f"{template_name}.html")
        return template.render(**context)
    except Exception as e:
        logger.error(f"Failed to render email template {template_name}: {e}")
        return ""

async def send_email(to: str, subject: str, html: str):
    """Sends an email using the Resend API."""
    api_key = os.environ.get("RESEND_API_KEY")
    mail_from = os.environ.get("MAIL_FROM", "onboarding@resend.dev")

    if not api_key:
        logger.warning("RESEND_API_KEY not set. Skipping email send.")
        return None

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "from": mail_from,
                    "to": [to],
                    "subject": subject,
                    "html": html
                }
            )
            response.raise_for_status()
            logger.info(f"Successfully sent email to {to}")
            return response.json()
    except Exception as e:
        logger.error(f"Failed to send email to {to} via Resend: {e}")
        return None

async def send_templated_email(to: str, email_type: str, context: dict):
    """Renders a template and sends it via Resend API."""
    html_content = render_email_template(email_type, context)
    if not html_content:
        logger.error(f"Cannot send email to {to}: Template {email_type} rendering failed.")
        return None

    subject_map = {
        "welcome": "Welcome to AI Productivity OS",
        "verify_email": "Verify your email",
        "password_reset": "Reset your password"
    }
    subject = subject_map.get(email_type, "Notification from AI Productivity OS")

    return await send_email(to, subject, html_content)
