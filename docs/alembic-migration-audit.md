# Alembic Migration Audit

## Executive Summary
A comprehensive audit of the Alembic migration history, definitions, and database schemas has been completed. The audit evaluated the synchronization between the SQLAlchemy models and the existing Alembic migration files, identified significant drift, and resolved missing tables and columns to establish a reliable upgrade path. We have also resolved idempotency issues in manual migration scripts and restored correct down-revision references without rewriting historical Alembic identifiers.

## Drift Findings
Previous reports incorrectly stated that no tables were missing and that the database schema was fully aligned with the models. Our audit uncovered the following discrepancies:
- **Missing Tables:** `opportunities`, `risk_classifications`, and `agent_recommendations` existed in models but had no migration to create them.
- **Drift Columns:** Over 40 columns across `ai_systems`, `users`, `workflows`, and `engineering_records` were added to the models but lacked migrations.
- **Foreign Key Mismatches:** Discrepancies between model definitions and the actual schema constraints.

All of the above have been resolved by adding `45d20f343cfe` (drift column resolution) and `a4da25a47216` (missing table creation).

## Schema Idempotency & Revision Graph
- **Idempotent Operations:** `manual_002` (handling safe deletion of a placeholder user), `manual_003` (enabling RLS on API tables), and `a4da25a47216` (dynamic role revocation via `EXECUTE`) have been updated to ensure rerunnability.
- **Pgvector Extension:** `CREATE EXTENSION IF NOT EXISTS vector` properly executes before vector-dependent objects are created in `ca6463a714d3_add_regulation_chunks.py`.
- **Graph Connection:** `9f8e7d6c5b4a_add_industry_type_to_audits.py` properly revisions `manual_001` and connects to the correct graph hierarchy.
- **Git Markers:** Fixed syntax drift and conflict markers inside `migration_helpers.py` and `manual_005_add_user_token_and_verification.py`.

## Validation via CI
- A CI validation workflow runs `alembic upgrade head`, `alembic check`, `alembic downgrade -1`, and `alembic upgrade head` inside a clean `pgvector/pgvector:pg16` database to guarantee schema safety.
- **Note:** Local validation via Docker was not successfully executed in this session due to environmental overlayfs issues; full validation relies on the GitHub Actions remote pipeline.

## How to Apply
To apply these migrations to a target environment, perform the following steps:
1. **Take a backup:** Always ensure a full database backup is taken before running schema migrations.
2. **Upgrade head:** Run `alembic upgrade head` from the `backend/` directory.
3. **Never run `create_all`:** The application relies on Alembic for schema state management; avoid using SQLAlchemy's `Base.metadata.create_all`.

**Warning:** Never stamp a database without manually comparing its schema to the migration chain (`alembic check`). Failing to do so can result in permanent schema divergence and silent data corruption.
