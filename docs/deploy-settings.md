# Deployment Settings

This document describes the deployment configuration for the AI Productivity OS application.

## Frontend

- Build command: `npm run build`
- Output directory: `dist` (Vite default)
- Node.js CI version: 18 (upgrade in a separate PR)
- Install command: `npm ci`

### Frontend environment variables

| Variable | Source |
|---|---|
| `VITE_API_URL` | `frontend/.env.example` |
| `VITE_APP_NAME` | `frontend/.env.example` |
| `VITE_APP_ENVIRONMENT` | `frontend/.env.example` |

`VITE_API_URL` must point to the deployed backend API.

## Backend

- Python version: 3.11
- Start command: `uvicorn main:app --host 0.0.0.0 --port 8080`
- Port: `8080`
- Docker health-check path: `/health`
- Readiness path: `/ready`

### Backend environment variables

| Variable | Source |
|---|---|
| `DATABASE_URL` | `backend/config.py` |
| `SECRET_KEY` | `backend/config.py` |
| `SUPABASE_URL` | `backend/config.py` |
| `SUPABASE_KEY` | `backend/config.py` |
| `REDIS_URL` | `backend/config.py` |
| `SENDGRID_API_KEY` | `backend/config.py` |
| `FRONTEND_URL` | `backend/config.py` |
| `ENVIRONMENT` | `backend/config.py` |
| `ALGORITHM` | `backend/config.py` |
| `CORS_ALLOW_ORIGINS` | `backend/config.py` |
| `CORS_ALLOW_ORIGIN_REGEX` | `backend/config.py` |
| `GEMINI_API_KEY1` | `backend/config.py` |
| `GEMINI_API_KEY2` | `backend/config.py` |
| `RESEND_API_KEY` | `backend/utils/email.py` |
| `MAIL_FROM` | `backend/utils/email.py` |
| `CELERY_TASK_ALWAYS_EAGER` | `backend/tests/conftest.py` |

## Health and readiness

- `GET /health` is the liveness check. It should return HTTP 200 without requiring a database query.
- `GET /ready` is the readiness check. It should execute a database query and return HTTP 503 if the database is unavailable or the check times out.
- The Docker health check targets `http://127.0.0.1:8080/health`.
- Render service health-check settings are configured in the Render dashboard.

## Continuous integration

- Backend tests use a disposable PostgreSQL service with the `pgvector` extension enabled.
- Backend lint runs `flake8 backend/`.
- Frontend CI uses `npm ci`, `npm run lint`, and `npm run build`.
- Frontend lint is advisory until existing lint errors are resolved. Frontend build remains a required check.
- Never use production database credentials or production secrets in CI.
- Keep deployment secrets in the relevant hosting provider's environment settings, not in source control.

