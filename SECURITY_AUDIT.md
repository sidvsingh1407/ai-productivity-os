# Security Audit: RLS Status

This document details the expected initial state of Row Level Security (RLS) on the tables within the TarkaX database. The database is hosted on Supabase and is managed by SQLAlchemy/Alembic.

## Current State Analysis
Based on a review of the current Alembic migration history (specifically, `alembic current` being expected to be prior to `7a8b9c0d1e2f` because it was not successfully applied by the CI/CD pipeline), RLS is currently **disabled** across all tables.

Furthermore, a new table `contact_leads` was added in a manual migration (`add_contact_leads_table.py`) but was never included in the proposed RLS enablement script `7a8b9c0d1e2f`.

| Table | RLS Enabled | Policies Present | Risk |
| ----- | ----------- | ---------------- | ---- |
| `users` | False | None | High |
| `organizations` | False | None | High |
| `org_members` | False | None | High |
| `invitations` | False | None | High |
| `audits` | False | None | High |
| `audit_versions` | False | None | High |
| `reports` | False | None | High |
| `workflows` | False | None | High |
| `export_jobs` | False | None | High |
| `subscriptions` | False | None | High |
| `blueprints` | False | None | High |
| `integration_results` | False | None | High |
| `billing_plans` | False | None | Medium |
| `contact_leads` | False | None | High |

**Risk Assessment:** Without RLS enabled and policies present to restrict access, any user with the Supabase `anon` key could theoretically interact with these tables via the public PostgREST API endpoint, bypassing the FastAPI application entirely. This is a critical security vulnerability.
