# RLS Policy Inventory

This document inventories the Row Level Security (RLS) policies implemented across all tables to restrict Supabase PostgREST access while maintaining full backend functionality.

## Applied Policy Details

For every public table, the following policy is applied:

**Policy Name:** `Allow backend access, deny postgrest`
**Policy Type:** `PERMISSIVE` for `ALL` commands (SELECT, INSERT, UPDATE, DELETE)
**Policy Purpose:** To block external API access via Supabase’s default PostgREST roles (`anon` and `authenticated`) while permitting backend service accounts (e.g., `postgres` or custom service roles) full access to manage records as handled by FastAPI.
**Expressions:**
- `USING (current_user NOT IN (anon, authenticated))`
- `WITH CHECK (current_user NOT IN (anon, authenticated))`

## Table Inventory

| Table Name | Policy Name | Policy Type | Purpose |
| ---------- | ----------- | ----------- | ------- |
| `users` | Allow backend access, deny postgrest | PERMISSIVE ALL | Block direct PostgREST API access |
| `organizations` | Allow backend access, deny postgrest | PERMISSIVE ALL | Block direct PostgREST API access |
| `org_members` | Allow backend access, deny postgrest | PERMISSIVE ALL | Block direct PostgREST API access |
| `invitations` | Allow backend access, deny postgrest | PERMISSIVE ALL | Block direct PostgREST API access |
| `audits` | Allow backend access, deny postgrest | PERMISSIVE ALL | Block direct PostgREST API access |
| `audit_versions` | Allow backend access, deny postgrest | PERMISSIVE ALL | Block direct PostgREST API access |
| `reports` | Allow backend access, deny postgrest | PERMISSIVE ALL | Block direct PostgREST API access |
| `workflows` | Allow backend access, deny postgrest | PERMISSIVE ALL | Block direct PostgREST API access |
| `export_jobs` | Allow backend access, deny postgrest | PERMISSIVE ALL | Block direct PostgREST API access |
| `subscriptions` | Allow backend access, deny postgrest | PERMISSIVE ALL | Block direct PostgREST API access |
| `blueprints` | Allow backend access, deny postgrest | PERMISSIVE ALL | Block direct PostgREST API access |
| `integration_results` | Allow backend access, deny postgrest | PERMISSIVE ALL | Block direct PostgREST API access |
| `billing_plans` | Allow backend access, deny postgrest | PERMISSIVE ALL | Block direct PostgREST API access |
| `contact_leads` | Allow backend access, deny postgrest | PERMISSIVE ALL | Block direct PostgREST API access |
