# Authorization Model Assessment

## Executive Summary
This document outlines the current authorization model for the TarkaX backend and how Supabase Row Level Security (RLS) policies fit into this architecture.

## Primary Authorization Path (FastAPI)
The TarkaX platform primarily handles authentication and authorization at the application layer via FastAPI dependencies.

1. **Authentication Path**: Clients authenticate via the `/auth/login` endpoint to receive a JWT access token. This token is passed in the `Authorization` header (`Bearer <token>`).
2. **Authorization Path**:
   - `get_current_user` decodes the JWT, extracts the user ID, and fetches the `User` record from the database. It enforces that the request is authenticated.
   - `get_current_org` fetches the `Organization` associated with the `User` via the `OrgMember` mapping table. It enforces that the user belongs to an organization.
3. **Database Access Path**: Once inside a route, the router handlers (e.g., in `backend/audits/router.py`) and repository methods (e.g., in `backend/audits/repository.py`) explicitly enforce organization isolation by appending `.where(Audit.org_id == org_id)` to SQLAlchemy queries.

This means that *by the time a query reaches PostgreSQL, FastAPI has already filtered the records to ensure cross-tenant data access is blocked.*

## RLS Interaction Model
Because the backend uses a long-lived database connection (often authenticated via a `postgres` or `service_role` equivalent connection string) without setting session variables like `current_user_id` for PostgreSQL, standard RLS policies that rely on `auth.uid()` (the Supabase native method) cannot natively see the FastAPI user context.

Therefore, the purpose of applying RLS in TarkaX is **not** to enforce tenant isolation at the backend level (which FastAPI already handles), but rather to **close the public API surface area exposed by Supabase PostgREST**.

The proposed policy:
```sql
CREATE POLICY "Allow backend access, deny postgrest" ON <table>
AS PERMISSIVE FOR ALL
USING (current_user NOT IN (anon, authenticated))
WITH CHECK (current_user NOT IN (anon, authenticated));
```
explicitly denies access to the default `anon` and `authenticated` roles used by PostgREST. This prevents anonymous or authenticated users from querying the database directly using `supabase-js` or PostgREST endpoints, while allowing the backend API (which connects as `postgres` or another backend role) unrestricted access to manage the data.

## Conclusion
The current architecture **does not rely on Supabase RLS for application-level authorization**. RLS serves strictly as a defense-in-depth measure to restrict direct database access via the Supabase API, ensuring all requests must pass through the FastAPI backend where proper validation and isolation are enforced.
