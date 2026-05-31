# AI Productivity OS

A Python + React monorepo for the AI Productivity Intelligence System.

## 1. Current project state
The repository is structured as a monorepo with `backend` and `frontend` directories.

**Root level files:**
- `README.md`
- `docker-compose.yml`
- `file_audit.txt`

**Backend (`/backend`)**
A FastAPI application using SQLAlchemy and asyncpg.
*   **Infrastructure & Config:** `Dockerfile`, `Procfile`, `requirements.txt`, `.env.example`, `config.py`, `database.py`, `dependencies.py`, `main.py`
*   **Database Migrations:** `alembic.ini`, `alembic/` (with two migrations in `versions/`: `3ff69d4ebaa6_initial_migration.py` and `5ed348e4f775_initial_models.py`)
*   **Models (`models/`):** `audit.py`, `billing.py`, `organization.py`, `report.py`, `user.py`, `workflow.py`
*   **Feature Modules:**
    *   `admin/` (router, schemas, service)
    *   `analytics/` (router, schemas, service)
    *   `audits/` (repository, router, schemas, scoring_engine, service)
    *   `auth/` (jwt_utils, password_utils, router, service)
    *   `billing/` (router)
    *   `integration/` (recommendation_engine, router, schemas, service)
    *   `organizations/` (repository, router, schemas, service)
    *   `reports/` (pdf_generator, router, schemas, service)
    *   `users/` (repository, router, schemas, service)
    *   `workflows/` (pipeline, repository, router, schemas, service, temp_models)
*   **Tasks:** `tasks/` (celery_app.py, email_tasks.py, pdf_tasks.py)
*   **Storage:** `storage/reports/`

**Frontend (`/frontend`)**
A React application built with Vite and TypeScript.
*   **Infrastructure & Config:** `package.json`, `vite.config.ts`, `tailwind.config.ts`, `tsconfig.json`, `vercel.json`
*   **Entry:** `index.html`, `src/main.tsx`, `src/App.tsx`, `src/index.css`
*   **Pages (`src/pages/`):** `Dashboard.tsx`, `LandingPage.tsx`, `NewAudit.tsx`, `NewWorkflow.tsx`, `Analytics.tsx`, `AuditDetail.tsx`, `AuditHistory.tsx`, `IntegrationResults.tsx`, `WorkflowDetail.tsx`, `Settings/Billing.tsx`, `Settings/OrgSettings.tsx`, `admin/AdminOrgs.tsx`, `admin/AdminUsers.tsx`
*   **Components (`src/components/`):** `DisclaimerModal.tsx`, `admin/AdminRoute.tsx`, `auth/PrivateRoute.tsx`, `charts/ScoreRadarChart.tsx`, `charts/ScoreTrendLine.tsx`, UI components (`ui/progress.tsx`, etc.), `layout/`
*   **State & API:** `src/store/authStore.ts`, `src/api/client.ts`

## 2. What is incomplete or missing
*   **Backend:**
    *   `reports/pdf_generator.py` references `generate_report` which is undefined (F821).
*   **Frontend Packages:** Several UI libraries referenced in code are missing from `package.json` and not installed:
    *   `framer-motion` (used in `DisclaimerModal.tsx`, `LandingPage.tsx`)
    *   `recharts` (used in `ScoreRadarChart.tsx`, `ScoreTrendLine.tsx`)
    *   `sonner` (used in `AdminRoute.tsx`, `Billing.tsx`, `OrgSettings.tsx`, `AdminUsers.tsx`)
    *   `@radix-ui/react-progress` (used in `ui/progress.tsx`)
*   **Frontend Import Paths:**
    *   Missing aliased imports: Cannot find module `@/lib/api` (used across `Analytics.tsx`, `OrgSettings.tsx`, `AdminOrgs.tsx`, `AdminUsers.tsx`).
    *   Broken imports: `import { apiClient } from "@/api/client"` fails because `apiClient` is a default export, not a named export.
*   **Frontend Type Errors:**
    *   Properties `is_superadmin` do not exist on the defined `User` type.
    *   `organization` does not exist on `AuthState`.
    *   Type mismatches in UI component props (e.g., passing `"success"` or `"warning"` to components that do not accept those variants).

## 3. Deployment status
**Frontend on Vercel**
*   **Env vars needed:** At minimum `VITE_API_URL` (usually maps to backend).
*   **Build command:** `npm run build` (which runs `tsc && vite build`)
*   **Output directory:** `dist`
*   **Configuration:** `vercel.json` is configured to rewrite all routes to `/index.html`.

**Backend on Render**
*   **Env vars needed:** `DATABASE_URL`, `SUPABASE_URL`, `SUPABASE_KEY`, `SECRET_KEY`, `REDIS_URL`, `SENDGRID_API_KEY`, `FRONTEND_URL`

**Database on Supabase**
*   **Migrations:** Must run Alembic migrations from the `backend/` directory (`alembic upgrade head`) to apply `3ff69d4ebaa6_initial_migration.py` and `5ed348e4f775_initial_models.py`.
*   **Tables:** The migrations will create tables corresponding to models: users, organizations, user_organizations, audits, workflows, reports, and billing/subscription tables.

## 4. Known issues
*   **Frontend Build Failure:** The frontend **cannot be deployed** currently because `npm run build` fails due to multiple missing packages (`framer-motion`, `recharts`, `sonner`, `@radix-ui/react-progress`), missing internal modules (`@/lib/api`), broken export signatures (`apiClient`), and strict TypeScript type errors (`is_superadmin`, missing props).
*   **Backend Syntax/Import Errors:** The backend has undefined names in `reports/pdf_generator.py` which will crash runtime execution of PDF generation tasks.

## 5. Next steps
1.  **Fix Frontend Dependencies:** Run `npm install framer-motion recharts sonner @radix-ui/react-progress` in the `frontend` directory.
2.  **Fix Frontend Imports & Types:**
    *   Correct the import of `apiClient` to `import apiClient from "@/api/client"`.
    *   Implement or stub the missing `@/lib/api` file.
    *   Update the `User` interface to include `is_superadmin?: boolean` and `AuthState` to include `organization`.
    *   Fix the strict type string matches for UI variants (e.g. replacing `"success"` with `"default"` or implementing the variants).
3.  **Fix Backend Code:** Resolve the undefined `generate_report` function in `backend/reports/pdf_generator.py`.
4.  **Verify Build:** Successfully run `npm run build` in the frontend and a successful start of the backend server locally before attempting cloud deployment.
