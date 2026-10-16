# Root-Cause Report: Product Instability post-3e552ae

## Overview
This report compares the stable state of commit `3e552ae` (June 5th) against the current `main` branch to identify the specific changes that led to login failures, registration failures, CORS issues, and routing issues.

## 1. Authentication Changes
- **Commit `fd91208`**: Removed the entire authentication system (`backend/auth/router.py`, `backend/auth/service.py`, `backend/auth/jwt_utils.py`, `frontend/src/api/auth.ts`) to implement a 'temporary access mode'.
- **Impact**: This completely broke normal registration and login flows, as the backend endpoints (`/auth/register`, `/auth/login`) no longer existed. The frontend store (`authStore.ts`) was decoupled from actual secure backend verification.

## 2. Database Schema Changes
- **Alembic Alterations**: Post-`3e552ae`, multiple schema migrations were altered or introduced, most notably the addition of `add_contact_leads_table.py` and `8d9e0f1g2h3i_add_invitation_schema.py`.
- **Auth Models**: User models and relationships were refactored out when the auth system was bypassed, causing any legacy database interactions relying on user UUIDs to fail.

## 3. RLS Policy Changes
- **PostgREST Hardening**: Although `3e552ae` pre-dated the complex RLS rollout, subsequent commits merged `P1_SECURITY_RLS.md` and altered `backend/admin/schemas.py` and `api_platform` routers to enforce restrictive Supabase row-level security policies.
- **Impact**: These policies prevented the API (and the 'temporary access mode') from reading or writing records because the application was no longer passing valid JWTs that the database required to evaluate RLS policies.

## 4. Routing Changes
- **Backend**: The `backend/main.py` and API routers were refactored. The `/auth` router was unmounted and replaced with `prompt_intelligence/router.py` and `api_platform/router.py`.
- **Frontend**: Routing components (`PrivateRoute.tsx`) were modified or bypassed, creating broken authentication loops where the frontend expected a valid token but the backend had no means to issue or validate it.

## 5. Deployment Configuration Changes
- **CORS**: Multiple commits attempted to 'fix' CORS (`8ca7f15`, `40796873...`). They moved away from liberal CORS policies to strict environment variable matching (`FRONTEND_URL`), which caused preflight failures when the deployment environment variables were misconfigured.
- **Impact**: The combination of missing auth endpoints and strict CORS meant that even if a frontend request was valid, it was often rejected by the backend before reaching the router.

## Root Cause Summary (Smallest Set of Commits)
The cascading failures were directly caused by:
1. **`2c4d649` & `8cd861f`**: The introduction of strict RLS and RBAC policies that demanded valid JWTs at the database level.
2. **`8ca7f15`**: The aggressive normalization of CORS requiring strict environment parity.
3. **`fd91208`**: The fatal decision to strip out the authentication endpoints to 'bypass' the complex security rollout. By removing `/auth/login` and `/auth/register` while the database still required valid RLS tokens, the application entered an unrecoverable state where users could neither register nor authenticate, resulting in ubiquitous access denial and routing failures.
