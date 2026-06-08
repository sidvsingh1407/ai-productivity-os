# Alembic Migration Audit

## Executive Summary
A comprehensive audit of the Alembic migration history, definitions, and database schemas has been completed. The audit evaluated the synchronization between the SQLAlchemy models and the existing Alembic migration files, looking for orphan migrations, missing definitions, conflicts, and tested the database upgrade path on a fresh PostgreSQL deployment.

## Deployment Readiness Assessment: **GO WITH RISKS**
The migration framework successfully reaches `head` from an empty PostgreSQL database. However, there is schema drift between the SQLAlchemy models and the database that creates structural risks and prevents local SQLite testing.

### P0 (Launch Blocking)
- **None.** A clean run of `alembic upgrade head` from an empty PostgreSQL database succeeds perfectly, confirming the structural integrity of the migration chain for production deployments.

### P1 (High Risk)
- **Type Mismatches (JSON vs JSONB):** Models declare fields as `JSON`, but migrations implemented them as `postgresql.JSONB`. This explicitly breaks local development using SQLite, as SQLite does not natively support `JSONB` in the SQLAlchemy compiler without `.with_variant()`. This applies to 10 columns across 7 tables (e.g., `audits.form_response`, `billing_plans.features`, `workflows.input_config`).
- **Foreign Key Mismatches:** 15 foreign key constraints across 11 tables differ between the model definition and the database schema (e.g., ON DELETE cascade differences, naming mismatches). Alembic check attempts to remove and recreate these.

### P2 (Technical Debt)
- **Nullability Drift:** 17 columns across various tables (e.g., `audits.user_id`, `blueprints.automation_tier`) have mismatched nullability rules. The database schema allows nulls (`True`), but the models require them (`False`), or vice versa.
- **Metadata/Docstring Inconsistencies:** Migration `6f5a34a2e5d9_add_evidence_and_confidence.py` specifies `Revises: 5ed348e4f775` in its docstring, but `5ed348e4f775` does not exist in the repository. Its actual programmatic `down_revision` correctly points to `3ff69d4ebaa6`, so this does not break execution but causes confusion.

---

## Detailed Findings

### Migration Status
- **Current Head:** `manual_003` (Enable RLS on api_keys and api_usage_logs)
- **Pending Migrations:** None (Database is currently up to date with the head).
- **Migration Conflicts:** None detected (Multiple heads were successfully merged in `05ac55cf989f`).

### Model vs Migration Mismatches

#### Missing / Extra Columns
- No columns are missing from the tables.
- No tables are entirely missing.

#### Type Mismatches
The following columns are typed as `JSON` in the models, but created as `JSONB` in the migrations:
1. `audit_versions.scores_snapshot`
2. `audits.form_response`
3. `audits.evidence_response`
4. `audits.scores`
5. `audits.contradictions`
6. `audits.compliance_risk_reasons`
7. `billing_plans.features`
8. `blueprints.blueprint_data`
9. `integration_results.recommendations`
10. `workflows.input_config`

#### Nullability Differences
The following columns have differing nullability (Model vs. Database):
1. `audit_versions.scores_snapshot`
2. `audits.user_id`
3. `audits.form_response`
4. `audits.compliance_risk_flag`
5. `billing_plans.max_users`
6. `billing_plans.features`
7. `blueprints.automation_tier`
8. `blueprints.industry_variant`
9. `blueprints.blueprint_data`
10. `blueprints.confidence`
11. `integration_results.recommendations`
12. `invitations.invited_by_user_id`
13. `reports.file_size`
14. `reports.expires_at`
15. `subscriptions.plan_id`
16. `workflows.user_id`
17. `workflows.input_config`

#### Foreign Key Mismatches
Alembic detects drift in the following Foreign Keys and suggests dropping/recreating them:
1. `audit_versions_audit_id_fkey` on `audit_versions`
2. `audits_org_id_fkey` on `audits`
3. `audits_user_id_fkey` on `audits`
4. `blueprints_workflow_id_fkey` on `blueprints`
5. `export_jobs_user_id_fkey` on `export_jobs`
6. `integration_results_audit_id_fkey` on `integration_results`
7. `integration_results_workflow_id_fkey` on `integration_results`
8. `invitations_org_id_fkey` on `invitations`
9. `org_members_user_id_fkey` on `org_members`
10. `org_members_org_id_fkey` on `org_members`
11. `reports_audit_id_fkey` on `reports`
12. `subscriptions_plan_id_fkey` on `subscriptions`
13. `subscriptions_org_id_fkey` on `subscriptions`
14. `workflows_user_id_fkey` on `workflows`
15. `workflows_org_id_fkey` on `workflows`

---

## Testing Evidence

### Clean Database Migration (PostgreSQL)
When executing `alembic upgrade head` from an entirely empty PostgreSQL database:
```text
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 3ff69d4ebaa6, Initial migration
INFO  [alembic.runtime.migration] Running upgrade 3ff69d4ebaa6 -> 6f5a34a2e5d9, Add evidence and confidence fields
...
INFO  [alembic.runtime.migration] Running upgrade manual_002 -> manual_003, Enable RLS on api_keys and api_usage_logs
```
**Conclusion:** The migration dependency chain is valid and completes successfully on production-grade infrastructure.

### Local SQLite Failure (Testing Constraints)
When running `alembic upgrade head` locally against the default SQLite setup (`sqlite+aiosqlite:///:memory:`):
```text
sqlalchemy.exc.CompileError: (in table 'billing_plans', column 'features'): Compiler <sqlalchemy.dialects.sqlite.base.SQLiteTypeCompiler object at 0x...> can't render element of type JSONB
```
**Root Cause:** `3ff69d4ebaa6_initial_migration.py` explicit uses `postgresql.JSONB()`.
**Recommended Fix:** Use `.with_variant(postgresql.JSONB, "postgresql")` combined with `JSON` in the models to ensure database-agnostic compilation.

### Orphan Docstring Reference
```text
$ cat backend/alembic/versions/6f5a34a2e5d9_add_evidence_and_confidence.py
"""Add evidence and confidence fields

Revision ID: 6f5a34a2e5d9
Revises: 5ed348e4f775
...
down_revision: Union[str, Sequence[str], None] = '3ff69d4ebaa6'
```
**Root Cause:** The `Revises:` docstring is out of sync and referencing a non-existent commit (`5ed348e4f775`), but the programmatic `down_revision` dependency is correct.
**Recommended Fix:** Update the docstring to match `down_revision` (`3ff69d4ebaa6`) to prevent developer confusion.
