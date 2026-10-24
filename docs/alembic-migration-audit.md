# Alembic Migration Audit

## Executive Summary
A comprehensive audit of the Alembic migration history, definitions, and database schemas has been completed. The audit evaluated the synchronization between the SQLAlchemy models and the existing Alembic migration files, identified significant drift, and resolved missing tables and columns to establish a reliable upgrade path.

## Drift Findings
Previous reports incorrectly stated that no tables were missing and that the database schema was fully aligned with the models. Our audit uncovered the following discrepancies:
- **Missing Tables:** `opportunities`, `risk_classifications`, and `agent_recommendations` existed in models but had no migration to create them.
- **Drift Columns:** Over 40 columns across `ai_systems`, `users`, `workflows`, and `engineering_records` were added to the models but lacked migrations.
- **Foreign Key Mismatches:** Discrepancies between model definitions and the actual schema constraints.

All of the above have been resolved by adding Migration A (schema drift resolution) and Migration B (missing table creation).

## How to Apply
To apply these migrations to a target environment, perform the following steps:
1. **Take a backup:** Always ensure a full database backup is taken before running schema migrations.
2. **Upgrade head:** Run `alembic upgrade head` from the `backend/` directory.
3. **Never run `create_all`:** The application relies on Alembic for schema state management; avoid using SQLAlchemy's `Base.metadata.create_all`.

**Warning:** Never stamp a database without manually comparing its schema to the migration chain (`alembic check`). Failing to do so can result in permanent schema divergence and silent data corruption.
