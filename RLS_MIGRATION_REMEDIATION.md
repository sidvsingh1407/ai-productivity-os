# RLS Migration Remediation & Rollout Plan

## Root Cause Analysis
The Supabase database currently lacks the Row Level Security (RLS) policies defined in migration `7a8b9c0d1e2f`.
This occurred because the automated CI/CD pipeline (`.github/workflows/cloud-run-deploy.yml`) and the application startup routine (`backend/main.py`) **do not execute Alembic migrations**.

Instead, the application startup uses `Base.metadata.create_all`, which only creates missing tables but cannot run raw SQL migrations or track the `alembic_version` state. Since the `7a8b9c0d1e2f` migration relies exclusively on explicit raw SQL (`op.execute`), it was never applied to the production database.

## Environment Variables Required
To run the migration against the Supabase database, you must supply the production connection string.
Supabase provides a Transaction pooler string, but for migrations (DDL), you must use the **Session pooler** or **Direct Connection** URL.

```bash
# Standard PostgreSQL URI format (Required for Alembic/SQLAlchemy async connection)
# Ensure the scheme is postgresql+asyncpg:// if your alembic.ini or env.py is configured to use it
export DATABASE_URL="postgresql+asyncpg://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres"

# Optional: if Alembic/FastAPI requires it to boot (though Alembic purely needs DATABASE_URL)
export SECRET_KEY="<production_secret_key>"
```

## Rollout Procedure
To safely apply the migration to the production Supabase database, follow these steps from your local machine or a secure administrative environment:

1. **Activate Virtual Environment and Install Dependencies**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install pydantic_settings asyncpg psycopg2-binary
   ```

2. **Set the Production Database Variable**
   ```bash
   # Replace with your actual Supabase direct connection string
   export DATABASE_URL="postgresql+asyncpg://postgres.[PROJECT_REF]:[PASSWORD]@aws-0-[REGION].pooler.supabase.com:5432/postgres"
   ```

3. **Verify Connection and Current State**
   ```bash
   alembic current
   ```
   *Expected Output: `6f5a34a2e5d9` or `<base>`. If it says `7a8b9c0d1e2f`, the migration is already applied.*

4. **Apply the Migration**
   ```bash
   alembic upgrade head
   ```
   *Alternatively, to be perfectly explicit:*
   ```bash
   alembic upgrade 7a8b9c0d1e2f
   ```

## Verification Queries
Execute these queries in the Supabase SQL Editor to confirm the changes:

**1. Check Alembic Revision**
```sql
SELECT version_num FROM alembic_version;
```
*Expected Output: `7a8b9c0d1e2f`*

**2. Verify RLS is Enabled**
```sql
SELECT relname, relrowsecurity
FROM pg_class
WHERE relname IN ('users', 'organizations', 'audits', 'workflows', 'reports', 'export_jobs', 'subscriptions', 'invitations', 'audit_versions', 'blueprints', 'integration_results', 'billing_plans', 'org_members');
```
*Expected Output: `relrowsecurity` should be `true` (or `t`) for all listed tables.*

**3. Verify Policies Created**
```sql
SELECT tablename, policyname, permissive, roles, cmd, qual, with_check
FROM pg_policies
WHERE policyname = 'Allow backend access, deny postgrest';
```
*Expected Output: One row per table, showing `roles = {PUBLIC}`, `cmd = ALL`, and the exact `qual` and `with_check` expressions excluding `anon` and `authenticated`.*

## Rollback Procedure
If the application experiences unexpected permission denied errors or fails to connect, immediately rollback the migration using Alembic:

1. **Ensure environment variables are still set.**
2. **Execute downgrade command:**
   ```bash
   cd backend
   alembic downgrade 6f5a34a2e5d9
   ```

To manually rollback via Supabase SQL Editor (if Alembic is unavailable):
```sql
-- Disable RLS and drop policies for all 13 tables
DO $$
DECLARE
    t text;
    tables text[] := ARRAY['users', 'organizations', 'org_members', 'audits', 'workflows', 'reports', 'export_jobs', 'subscriptions', 'invitations', 'audit_versions', 'blueprints', 'integration_results', 'billing_plans'];
BEGIN
    FOREACH t IN ARRAY tables
    LOOP
        EXECUTE format('DROP POLICY IF EXISTS "Allow backend access, deny postgrest" ON %I;', t);
        EXECUTE format('ALTER TABLE %I DISABLE ROW LEVEL SECURITY;', t);
    END LOOP;
END $$;
```