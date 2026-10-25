import pytest
from unittest.mock import patch, MagicMock
from monitoring.sentry import init_sentry, _scrub_sensitive_data
from config import settings

def test_sentry_disabled_when_no_dsn():
    """Test that Sentry does not initialize and does not crash when DSN is empty."""
    with patch("monitoring.sentry.settings.SENTRY_DSN", ""):
        with patch("sentry_sdk.init") as mock_init:
            result = init_sentry()
            assert result is False
            mock_init.assert_not_called()

def test_sentry_initializes_with_dsn():
    """Test that Sentry initializes when a DSN is provided."""
    with patch("monitoring.sentry.settings.SENTRY_DSN", "https://public@sentry.example.com/1"):
        with patch("sentry_sdk.init") as mock_init:
            result = init_sentry()
            assert result is True
            mock_init.assert_called_once()

            # Verify basic configs passed
            kwargs = mock_init.call_args[1]
            assert kwargs["dsn"] == "https://public@sentry.example.com/1"
            assert kwargs["send_default_pii"] is False
            assert "before_send" in kwargs

def test_sentry_scrub_sensitive_data():
    """Test the data scrubbing hook to ensure secrets are filtered."""
    event = {
        "request": {
            "headers": {
                "Authorization": "Bearer secret_token",
                "Cookie": "session_id=123",
                "User-Agent": "test-agent"
            },
            "cookies": {
                "jwt": "super-secret-jwt",
                "safe_cookie": "hello"
            },
            "data": {
                "password": "my_password",
                "email_contents": "Hello World",
                "public_field": "safe_data"
            }
        }
    }

    scrubbed_event = _scrub_sensitive_data(event, None)

    req = scrubbed_event["request"]

    # Headers
    assert req["headers"]["Authorization"] == "[Filtered]"
    assert req["headers"]["Cookie"] == "[Filtered]"
    assert req["headers"]["User-Agent"] == "test-agent"

    # Cookies
    assert req["cookies"]["jwt"] == "[Filtered]"
    assert req["cookies"]["safe_cookie"] == "[Filtered]" # We blanket-scrub all cookies in our implementation, which is very safe

    # Body data
    assert req["data"]["password"] == "[Filtered]"
    assert req["data"]["email_contents"] == "[Filtered]"
    assert req["data"]["public_field"] == "safe_data"
