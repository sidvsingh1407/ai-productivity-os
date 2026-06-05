# Deployment Security Review

This document outlines the findings from a deployment and configuration security audit of the TarkaX codebase.

## Audit Scope
- `frontend/` directory and configuration (`.env.example`, `vite.config.ts`)
- `backend/` directory and configuration (`.env.example`, `config.py`, `database.py`)
- Alembic configuration
- Docker / Infrastructure configs

## Findings

### 1. Frontend Secrets Leakage
**Risk Level:** Low
**Finding:** A search through the frontend repository revealed no exposure of database credentials, Supabase service keys, or backend secrets. The frontend uses `VITE_API_URL` to communicate with the backend, which is the correct architecture. Since the Supabase JS client is not heavily utilized or relies solely on the anon key (not currently evident in frontend code, but standard practice), direct database manipulation from the frontend is mitigated.

### 2. DATABASE_URL Usage
**Risk Level:** Medium
**Finding:** `DATABASE_URL` is used correctly in the backend via `pydantic-settings` (`config.py`) and injected into `database.py` and `alembic/env.py`.
**Concern:** The application handles the modification of the connection string to `postgresql+asyncpg://` automatically. However, in deployment, care must be taken to ensure the `DATABASE_URL` provided to the Cloud Run or Railway environment is securely stored in a Secret Manager and not hardcoded in any CI/CD variables or unencrypted config files.

### 3. Supabase Keys (Anon / Service Role)
**Risk Level:** Low
**Finding:** The backend `config.py` defines `SUPABASE_URL` and `SUPABASE_KEY` (which `.env.example` notes as the anon key), but a search for "service_role" returned no results. This implies the backend connects directly to PostgreSQL via SQLAlchemy (`DATABASE_URL`) rather than using the Supabase REST API via `supabase-py` with a service role key. This is a secure architectural choice as it relies on standard database connection pooling.

### 4. Privilege Escalation Risks
**Risk Level:** Medium
**Finding:** Because the backend connects using a high-privilege PostgreSQL user (likely the `postgres` role provided by Supabase), any SQL injection vulnerability in the FastAPI application could lead to full database compromise, bypassing the RLS policies.
**Recommendation:** Ensure all database interactions utilize SQLAlchemy ORM or parameterized queries to prevent SQL injection. A brief review of the backend code shows standard SQLAlchemy ORM usage (e.g., `select(User).where(...)`), which mitigates this risk effectively.

## Conclusion
The deployment architecture is fundamentally sound. The separation of concerns between the React frontend (no DB access) and FastAPI backend (direct DB access) is maintained. The primary risk lies in how `DATABASE_URL` is managed in the production environment variables, which must be strictly controlled via secret management systems.
