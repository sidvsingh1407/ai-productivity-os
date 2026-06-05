-- SECURITY_VERIFICATION_QUERIES.sql
-- Copy-paste these queries into the Supabase SQL Editor to verify the security rollout.

-- 1. Verify current revision
-- Confirms the alembic migration was successfully applied.
SELECT version_num
FROM alembic_version;
-- Expected output: 7a8b9c0d1e2f

-- 2. Verify RLS enabled (and 4. Verify protected tables)
-- Checks that all relevant tables have Row Level Security enabled.
SELECT
    relname AS table_name,
    relrowsecurity AS rls_enabled
FROM pg_class
WHERE relname IN (
    'users', 'organizations', 'org_members', 'audits', 'workflows',
    'reports', 'export_jobs', 'subscriptions', 'invitations',
    'audit_versions', 'blueprints', 'integration_results', 'billing_plans',
    'contact_leads'
) AND relnamespace = (SELECT oid FROM pg_namespace WHERE nspname = 'public')
ORDER BY relname;
-- Expected output: All 14 tables should return `true` (or `t`) for `rls_enabled`.

-- 3. List policies (and 5. Verify policy coverage)
-- Ensures the correct policy is applied to each table and denies PostgREST roles.
SELECT
    tablename AS table_name,
    policyname AS policy_name,
    permissive AS is_permissive,
    roles,
    cmd,
    qual AS using_expression,
    with_check AS with_check_expression
FROM pg_policies
WHERE schemaname = 'public'
  AND tablename IN (
    'users', 'organizations', 'org_members', 'audits', 'workflows',
    'reports', 'export_jobs', 'subscriptions', 'invitations',
    'audit_versions', 'blueprints', 'integration_results', 'billing_plans',
    'contact_leads'
)
ORDER BY tablename;
-- Expected output: Each table should have the policy "Allow backend access, deny postgrest"
-- with cmd = ALL, and expressions verifying `current_user NOT IN ('anon', 'authenticated')`.
