# Security Audit & RLS Policy Design

## 1. Affected Tables
The following tables will have Row Level Security (RLS) enabled:
- `users`
- `organizations`
- `org_members`
- `audits`
- `workflows`
- `reports`
- `export_jobs`
- `subscriptions`
- `invitations`
- `audit_versions`
- `blueprints`
- `integration_results`
- `billing_plans`

## 2. Policy Design

**Objective:** Fulfill Supabase Security Advisor recommendations by enabling RLS to prevent unauthorized access via PostgREST APIs, while ensuring the FastAPI backend retains full access.

**Strategy:**
- We will enable RLS on all tables.
- By default in PostgreSQL, enabling RLS without policies results in a "default deny" for all operations for standard roles.
- Roles with the `BYPASSRLS` attribute (such as the default `postgres` superuser used in `.env.example`) or the table owner bypass RLS automatically.
- To ensure robustness and specifically target the vulnerability (exposure of PostgREST APIs), we will enable RLS. Because we are not providing policies for `anon` or `authenticated`, Supabase's PostgREST will deny access to these tables.
- The FastAPI backend connecting as `postgres` will bypass RLS.
- If the FastAPI backend is using a non-superuser role that does not bypass RLS, we will explicitly create a policy to allow all operations for that connection user, OR simply a policy that denies `anon` and `authenticated` but allows others.

Given the constraints to not break FastAPI + SQLAlchemy access and avoid transaction context changes, we will:
1. `ALTER TABLE <table_name> ENABLE ROW LEVEL SECURITY;`
2. Explicitly create a policy allowing the Postgres roles that are *not* `anon` or `authenticated` (to cover all backend potential roles safely).

```sql
CREATE POLICY "Allow backend access, deny postgrest" ON <table_name>
AS PERMISSIVE FOR ALL
USING (current_user NOT IN ('anon', 'authenticated'))
WITH CHECK (current_user NOT IN ('anon', 'authenticated'));
```

This guarantees that:
- `anon` and `authenticated` via PostgREST are blocked.
- Any backend connection (e.g. `postgres`, or a custom pooling role) is allowed, maintaining application stability.

## 3. Risk Assessment

- **Risk of Production Lockout:** Negligible. The explicit policy allows any user that isn't the Supabase PostgREST default roles to operate normally.
- **Risk of PostgREST Abuse:** Eliminated. `anon` and `authenticated` roles will fail the policy check.
- **Invitations Token Exposure:** Eliminated. The `invitations` table will be inaccessible via PostgREST. The backend FastAPI application remains the sole gatekeeper for this data.

## 4. Rollback Strategy

The Alembic migration includes a `downgrade()` method that performs:
`ALTER TABLE <table_name> DISABLE ROW LEVEL SECURITY;`
`DROP POLICY IF EXISTS "Allow backend access, deny postgrest" ON <table_name>;`
This instantly restores the previous behavior.

## 5. Publicly Readable Tables

There are no tables that should remain publicly readable via Supabase PostgREST APIs. All database access must flow through the FastAPI application layer.
