# Deploy Settings

- Python version: 3.11
- Build command: `npm run build`
- Start command: `uvicorn main:app --host 0.0.0.0 --port 8080`
- Port: 8080
- Health path: `/health`
- Ready path: `/ready`

## Environment Variables

| name | read in (file) | purpose in one line | required (yes/no) | default exists (yes/no) |
| --- | --- | --- | --- | --- |
| DATABASE_URL | `backend/config.py` | Connection string for Postgres database | yes | no |
| SUPABASE_URL | `backend/config.py` | URL for Supabase integration | no | yes |
| SUPABASE_KEY | `backend/config.py` | Key for Supabase integration | no | yes |
| SECRET_KEY | `backend/config.py` | Secret key for JWT and cryptography | yes | no |
| REDIS_URL | `backend/config.py` | Connection string for Redis | no | yes |
| SENDGRID_API_KEY | `backend/config.py` | API key for SendGrid | no | yes |
| FRONTEND_URL | `backend/config.py` | Primary allowed frontend origin | no | yes |
| ENVIRONMENT | `backend/config.py` | Application environment (e.g. development) | no | yes |
| ALGORITHM | `backend/config.py` | Algorithm for JWT | no | yes |
| CORS_ALLOW_ORIGINS | `backend/config.py` | Comma-separated list of extra allowed origins | no | yes |
| CORS_ALLOW_ORIGIN_REGEX | `backend/config.py` | Regex for dynamically allowing origins | no | yes |
| GEMINI_API_KEY1 | `backend/config.py` | API key for Google Gemini (primary) | no | yes |
| GEMINI_API_KEY2 | `backend/config.py` | API key for Google Gemini (secondary) | no | yes |
| RESEND_API_KEY | `backend/utils/email.py` | API key for Resend emails | no | no |
| MAIL_FROM | `backend/utils/email.py` | Default from address for emails | no | yes |
| CELERY_TASK_ALWAYS_EAGER | `backend/tests/conftest.py` | Forces Celery tasks to run synchronously in tests | no | no |
| VITE_API_URL | `frontend/.env.example` | Backend API URL for frontend | no | no |
| VITE_APP_NAME | `frontend/.env.example` | Name of the frontend app | no | no |
| VITE_APP_ENVIRONMENT | `frontend/.env.example` | Frontend environment context | no | no |

The Render service settings live in the Render dashboard and not in this repo.
Render uses its own health check path setting. Set it to /health or /ready in the dashboard.
