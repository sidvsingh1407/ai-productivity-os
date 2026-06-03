# Apply Migration 7a8b9c0d1e2f to Supabase

This document provides the exact SQL, procedure, and verification queries to apply Alembic migration `7a8b9c0d1e2f` directly to Supabase. This is necessary because Supabase does not contain the `alembic_version` table, RLS is disabled, and deployments do not run Alembic migrations automatically.

## 1. Exact SQL generated from migration 7a8b9c0d1e2f

Because the `alembic_version` table does not exist in Supabase, the generated update to this table (`UPDATE alembic_version SET version_num='7a8b9c0d1e2f'...`) must be removed to prevent failure, or you will need to create the table and seed it. Assuming you are only trying to apply the schema/security changes as requested and not fully sync Alembic state right now, here is the exact SQL *without* the `alembic_version` table update:

```sql
BEGIN;

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON users
    AS PERMISSIVE FOR ALL
    USING (current_user NOT IN ('anon', 'authenticated'))
    WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE organizations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON organizations
    AS PERMISSIVE FOR ALL
    USING (current_user NOT IN ('anon', 'authenticated'))
    WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE org_members ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON org_members
    AS PERMISSIVE FOR ALL
    USING (current_user NOT IN ('anon', 'authenticated'))
    WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE audits ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON audits
    AS PERMISSIVE FOR ALL
    USING (current_user NOT IN ('anon', 'authenticated'))
    WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE workflows ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON workflows
    AS PERMISSIVE FOR ALL
    USING (current_user NOT IN ('anon', 'authenticated'))
    WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE reports ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON reports
    AS PERMISSIVE FOR ALL
    USING (current_user NOT IN ('anon', 'authenticated'))
    WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE export_jobs ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON export_jobs
    AS PERMISSIVE FOR ALL
    USING (current_user NOT IN ('anon', 'authenticated'))
    WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON subscriptions
    AS PERMISSIVE FOR ALL
    USING (current_user NOT IN ('anon', 'authenticated'))
    WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE invitations ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON invitations
    AS PERMISSIVE FOR ALL
    USING (current_user NOT IN ('anon', 'authenticated'))
    WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE audit_versions ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON audit_versions
    AS PERMISSIVE FOR ALL
    USING (current_user NOT IN ('anon', 'authenticated'))
    WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE blueprints ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON blueprints
    AS PERMISSIVE FOR ALL
    USING (current_user NOT IN ('anon', 'authenticated'))
    WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE integration_results ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON integration_results
    AS PERMISSIVE FOR ALL
    USING (current_user NOT IN ('anon', 'authenticated'))
    WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

ALTER TABLE billing_plans ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow backend access, deny postgrest" ON billing_plans
    AS PERMISSIVE FOR ALL
    USING (current_user NOT IN ('anon', 'authenticated'))
    WITH CHECK (current_user NOT IN ('anon', 'authenticated'));

COMMIT;
```

## 2. Safe procedure for applying it directly to Supabase

1. Open the Supabase Dashboard for your project.
2. Navigate to the **SQL Editor** on the left sidebar.
3. Click **New Query** to create a blank SQL snippet.
4. Copy and paste the SQL script provided in section 1 above.
5. Click the **Run** button (or press `Cmd+Enter` / `Ctrl+Enter`).
6. Wait for the "Success" confirmation toast.

## 3. Prerequisites and Risks

**Prerequisites:**
* You must have administrative access to the Supabase Dashboard for this project.
* The tables listed (`users`, `organizations`, `org_members`, `audits`, `workflows`, `reports`, `export_jobs`, `subscriptions`, `invitations`, `audit_versions`, `blueprints`, `integration_results`, `billing_plans`) must already exist in the `public` schema (which should be the case since this is applying a subsequent migration).

**Risks:**
* **Immediate Blocking of Front-end Clients:** This migration explicitly drops access for the `anon` and `authenticated` roles used by Supabase PostgREST. If any frontend code currently relies directly on `supabase-js` database queries (e.g., `supabase.from('users').select('*')`), these queries will immediately start returning permission denied or empty sets.
* **Alembic State Divergence:** Because we are running this SQL manually without the `alembic_version` table update, the database schema will be out-of-sync with what Alembic *thinks* the state is. If you later attempt to run `alembic upgrade head`, it will attempt to recreate these policies and potentially error out if not handled carefully.

## 4. Verification Queries

Run the following queries in the Supabase SQL Editor after applying the migration to verify success.

**Verify `rowsecurity = true`:**
```sql
SELECT
    relname AS table_name,
    relrowsecurity AS rowsecurity
FROM pg_class
WHERE relname IN (
    'users', 'organizations', 'org_members', 'audits', 'workflows',
    'reports', 'export_jobs', 'subscriptions', 'invitations',
    'audit_versions', 'blueprints', 'integration_results', 'billing_plans'
) AND relnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')
ORDER BY relname;
```
*(All 13 tables should return `true` for the `rowsecurity` column).*

**Verify `policies present`:**
```sql
SELECT
    tablename AS table_name,
    policyname AS policy_name,
    permissive AS is_permissive,
    roles,
    cmd,
    qual AS using_expression,
    with_check AS with_check_expression
FROM pg_policies
WHERE tablename IN (
    'users', 'organizations', 'org_members', 'audits', 'workflows',
    'reports', 'export_jobs', 'subscriptions', 'invitations',
    'audit_versions', 'blueprints', 'integration_results', 'billing_plans'
) AND schemaname = 'public'
ORDER BY tablename;
```
*(Each table should have the `Allow backend access, deny postgrest` policy listed).*
