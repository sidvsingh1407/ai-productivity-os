# TarkaX Phase 1 - Multi-User Organizations Audit

## Introduction
This document contains the Current State Audit of the TarkaX platform as part of Phase 1 of Sprint 6B.

## A. Do organizations already exist?
Yes, organizations already exist. The `Organization` model is defined in `backend/models/organization.py`, and when a user registers, an organization is automatically created and linked to the new user in `backend/auth/service.py` (`register_user`).

## B. Do org_members already enforce organization membership?
`OrgMember` enforces membership in terms of data schema (linking `User` to `Organization`), and the `get_current_org` dependency in `backend/dependencies.py` ensures that a user can only interact with the API if they belong to an organization. However, a user currently only belongs to one organization in `get_current_org` (it grabs the first one it finds: `result.scalar_one_or_none()`).

## C. Are audits linked to organizations?
Yes, audits are linked to organizations. The `Audit` model in `backend/models/audit.py` has an `org_id` column as a `ForeignKey("organizations.id")`.

## D. Are workflows linked to organizations?
Yes, workflows are linked to organizations. The `Workflow` model in `backend/models/workflow.py` has an `org_id` column as a `ForeignKey("organizations.id")`.

## E. Are reports linked to organizations?
Reports themselves (in `backend/models/report.py`) are linked to an `audit_id`, which indirectly links them to an organization. Furthermore, export jobs (`ExportJob`) are linked to `user_id`.

## F. Does any backend permission checking already exist, or is access currently enforced only in the UI?
Basic API endpoints use `get_current_org` which restricts data access to the current user's organization (e.g. `audits/router.py` passes `current_org.id` to repository functions). However, fine-grained role-based access control (RBAC) is almost nonexistent in the backend:
- `require_role(required_role)` exists in `backend/dependencies.py` but is a stub: `return current_user`. It does not actually verify the `OrgMember.role`.
- `backend/organizations/router.py` applies `require_role("admin")` as a dependency, but because it is a stub, any authenticated user can effectively access these endpoints.
- Thus, role-based access is primarily unenforced on the backend right now.

## Current State Matrix

| Area | Current State | Gap | Severity |
| ---- | ------------- | --- | -------- |
| **Organizations** | `Organization` model exists and is created on registration. | Support for multiple organizations per user exists in models but `get_current_org` assumes a single organization. No UI to switch orgs. | Low |
| **Users** | `User` model exists. | Users are tied to an org via `OrgMember`. Registration forces new org creation. | Low |
| **Roles** | `OrgRole` enum has `admin` and `member`. | Missing `owner` and `viewer` roles. Needs DB migration. | High |
| **Permissions** | `require_role` dependency is a stub. | No real backend RBAC. Users with `member` role can act as `admin`. | High |
| **Invitations** | `Invitation` model exists (`org_id`, `email`, `token`, `expires_at`, `accepted_at`). | Missing `role`, `invited_by`, `status`, `created_at` fields. No working email dispatch or UI flow. | High |
| **UI** | Basic Org Settings exist in `frontend/src/pages/Settings/OrgSettings.tsx`. | Missing Members Management page, Invite User flow, Role Management. | Medium |

## Missing Capabilities
1. Backend RBAC: `require_role` needs to actually check the user's role within the specific organization.
2. Models: `OrgRole` enum needs `owner` and `viewer`.
3. Models: `Invitation` needs new fields: `role`, `invited_by_user_id` (FK), `status` (enum), `created_at`.
4. API: Accept invitation endpoint logic is missing.
5. UI: Organization member management and invitation UI.

## Migration Risks
1. **OrgRole Enum Update:** Modifying a PostgreSQL ENUM type can be tricky depending on the database engine. Since SQLAlchemy is used with Alembic, we need to alter the type properly (e.g., using `ALTER TYPE ... ADD VALUE` in raw SQL for Postgres, or recreating the enum depending on SQLite/Postgres support).
2. **Invitation Schema Changes:** Adding non-nullable fields to `Invitation` without default values for existing rows will break migrations. We need to handle default values or make them nullable initially if there are existing records.

## Recommended Implementation Sequence
1. Create `ROLE_MATRIX.md` as per Phase 2.
2. Implement DB Migrations for `OrgRole` and `Invitation` models. (Phase 2 & 4 prep)
3. Implement actual role verification in `backend/dependencies.py` -> `require_role`. (Phase 3)
4. Update `Organization` backend APIs (Invitations, Roles). (Phase 4)
5. Build the UI for Organization Management, Members Page, and Invitations. (Phase 5 & 6)
6. Conduct Security Validation. (Phase 7)
