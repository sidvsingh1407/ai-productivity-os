# Supabase Security Advisor Status

This document captures the expected findings of the Supabase Security Advisor before and after the Sprint 6A remediations.

## BEFORE REMEDIATION (Current State)
Based on the lack of applied RLS migrations, the Supabase Security Advisor is expected to flag multiple high-severity issues:

* **Finding:** RLS Disabled on Public Tables
  * **Severity:** High
  * **Affected Tables:** `users`, `organizations`, `org_members`, `invitations`, `audits`, `audit_versions`, `reports`, `workflows`, `export_jobs`, `subscriptions`, `blueprints`, `integration_results`, `billing_plans`, `contact_leads`.
  * **Risk:** Data can be freely read, modified, or deleted by anyone with the `anon` key via PostgREST.

* **Finding:** Missing Policy Coverage
  * **Severity:** High
  * **Risk:** Tables lack any policies dictating who can perform SELECT, INSERT, UPDATE, or DELETE operations.

## AFTER REMEDIATION (Expected State)
After successfully applying the migration `7a8b9c0d1e2f` (which now includes `contact_leads`), the expected Security Advisor findings are:

* **Finding:** RLS Disabled on Public Tables
  * **Severity:** Resolved (0 tables affected)

* **Finding:** Missing Policy Coverage
  * **Severity:** Resolved (All public tables now have the "Allow backend access, deny postgrest" policy).

## Remaining Risks
While the Security Advisor findings regarding RLS will be resolved, the following architectural realities must be acknowledged:
1. **Application-Layer Reliance:** The security of tenant isolation completely relies on the FastAPI application code correctly passing and enforcing `org_id` in SQLAlchemy queries. RLS is not acting as a fallback for tenant isolation here; it is purely blocking the Supabase API.
2. **Backend Compromise:** If the backend environment (`DATABASE_URL`) is compromised, the attacker has unrestricted access to the database, as the backend role is exempt from the PostgREST RLS restrictions.
