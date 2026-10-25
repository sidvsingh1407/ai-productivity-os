import logging
import sentry_sdk
from config import settings

logger = logging.getLogger(__name__)

SENSITIVE_KEYS = {
    "password",
    "secret",
    "token",
    "authorization",
    "cookie",
    "jwt",
    "api_key",
    "apikey",
    "access_token",
    "refresh_token",
    "verification_token",
    "signature",
    "email_contents",
}

def _scrub_sensitive_data(event, hint):
    """
    Remove sensitive data from Sentry events before they are sent.
    """
    if "request" in event:
        request = event["request"]

        # Scrub headers
        if "headers" in request:
            for header_key in list(request["headers"].keys()):
                if header_key.lower() in SENSITIVE_KEYS:
                    request["headers"][header_key] = "[Filtered]"

        # Scrub cookies
        if "cookies" in request:
            for cookie_key in list(request["cookies"].keys()):
                request["cookies"][cookie_key] = "[Filtered]"

        # Scrub data
        if "data" in request and isinstance(request["data"], dict):
            for data_key in list(request["data"].keys()):
                if data_key.lower() in SENSITIVE_KEYS:
                    request["data"][data_key] = "[Filtered]"

    return event


def init_sentry():
    """
    Initializes Sentry if a DSN is provided.
    Does not crash if DSN is missing or empty.
    """
    dsn = settings.SENTRY_DSN

    if not dsn:
        logger.info("SENTRY_DSN is not set. Sentry monitoring is disabled.")
        return False

    try:
        environment = settings.SENTRY_ENVIRONMENT or settings.ENVIRONMENT or "development"

        sentry_sdk.init(
            dsn=dsn,
            environment=environment,
            release=settings.SENTRY_RELEASE if settings.SENTRY_RELEASE else None,
            before_send=_scrub_sensitive_data,
            # Disable noisy defaults for now
            traces_sample_rate=0.0,
            profiles_sample_rate=0.0,
            send_default_pii=False,
        )
        logger.info(f"Sentry initialized for environment: {environment}")
        return True
    except Exception as e:
        # Failsafe: Application must not crash if Sentry fails to initialize
        logger.error(f"Failed to initialize Sentry: {e}")
        return False
