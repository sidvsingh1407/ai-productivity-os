# Optional Sentry Monitoring Integration

This repository includes optional support for Sentry telemetry and error monitoring for both the backend (FastAPI) and frontend (React/Vite).

## Core Design Principles
* **100% Optional:** The application continues to start and function normally without any Sentry configuration. Telemetry errors will not crash the application.
* **Privacy by Default:** Aggressive payload scrubbers block sensitive configuration, passwords, cookies, authorization headers, JWTs, and keys.
* **Performance:** Telemetry tracing and profiling are disabled by default to avoid overwhelming free or self-hosted Sentry tiers with noisy transaction data.

## Configuration

Sentry monitoring is activated exclusively by providing a Sentry DSN environment variable.

### Backend (`backend/.env`)

```env
# Set this to a valid DSN to enable Sentry
SENTRY_DSN=
# Optional overrides
SENTRY_ENVIRONMENT=development
SENTRY_RELEASE=
```

### Frontend (`frontend/.env`)

```env
# Set this to a valid DSN to enable Sentry
VITE_SENTRY_DSN=
# Optional overrides
VITE_SENTRY_ENVIRONMENT=development
VITE_SENTRY_RELEASE=
```

## Privacy & Security Filters

We utilize Sentry's `before_send` hook to mutate the event payload before dispatching. Specifically, the integration searches dictionaries under `request.headers`, `request.cookies`, and `request.data`.

It identifies sensitive payload fields case-insensitively using the following heuristic matches:
- `password`, `secret`, `token`, `authorization`, `cookie`, `jwt`, `api_key`, `apikey`, `access_token`, `refresh_token`, `verification_token`, `signature`, `email_contents`.

Any identified value is rewritten to `[Filtered]`.

**NOTE:** In the backend `sentry.py` integration, `send_default_pii` is heavily restricted, and on the frontend, standard cookie tracking is disabled.

## Testing the integration locally

You do not need a live Sentry instance or active DSN to test local behavior. When the DSN variables are left blank or absent (default), the Sentry integrations securely short-circuit execution.

To run the telemetry unit tests:
```bash
cd backend
DATABASE_URL="sqlite+aiosqlite:///tarkax.db" SECRET_KEY="test" pytest tests/test_sentry.py
```
