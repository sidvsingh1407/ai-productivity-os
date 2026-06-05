# Sprint 6B-B — Permission Engine Design

## 1. Current Permission Implementation
Currently, permissions are heavily reliant on basic authentication (`get_current_user`) and general organization association (`get_current_org`). The system correctly maps an authenticated request token to a `User` and ensures the user belongs to at least one `Organization` via `OrgMember`.
However, once inside the organization boundary, access is unsegmented by role. Every member is treated equally within the context of their own organization's resources.

## 2. Existing `require_role()` Behavior
The `require_role()` function in `backend/dependencies.py` is fully stubbed. It currently accepts `required_role: str` as an argument but the inner `role_checker` merely depends on `get_current_user` and returns the `current_user` object. It **does not query the `OrgMember` table**, nor does it check the `role` enum. Any valid authenticated user will pass this dependency check, rendering it functionally useless for authorization.

## 3. Existing Authorization Middleware
There is no dedicated authorization middleware. The authorization layer relies entirely on FastAPI dependencies attached to routers or specific endpoints.
- `get_current_user` verifies the JWT and retrieves the `User`.
- `get_current_org` uses `get_current_user`, queries the `OrgMember` mapping table, and yields an `Organization`. It fails if the user belongs to no organization.
- `require_superadmin` effectively limits access to superusers via `is_superadmin` field on the `User`.

## 4. Endpoints Currently Unprotected (or Underprotected)
Any endpoint that requires specialized privileges but only uses `get_current_org` or the stubbed `require_role` is underprotected. These currently include:
- `organizations/router.py`:
  - `GET /organizations/members`
  - `POST /organizations/invite`
  - `DELETE /organizations/members/{user_id}`
- `audits/router.py`: All endpoints. Any member can create audits, view any audit in the org, and view any version.
- `workflows/router.py`: All endpoints. Any member can create workflows and view workflows.
- `reports/router.py`: All endpoints. Any member can generate or download reports.
- `billing/router.py`: Assuming billing routes rely on the same underprotected org checks.

## 5. Endpoints Requiring Roles
Once the new roles (`owner`, `admin`, `member`, `viewer`) are established, the following requirements should be mapped:

### Owner
- **Organizations:**
  - `DELETE /organizations/{id}` (if implemented in the future)
  - `PUT/PATCH /organizations/{id}` (manage org settings/name)
  - Change Member roles (including assigning other owners).
- **Billing:**
  - `POST /billing/subscription`, `DELETE /billing/subscription`, etc.
- **Includes all Admin privileges.**

### Admin
- **Organizations:**
  - `POST /organizations/invite`
  - `DELETE /organizations/members/{user_id}`
  - `GET /organizations/members`
- **Audits & Workflows:**
  - Delete audits or workflows (if those endpoints are added).
- **Includes all Member privileges.**

### Member
- **Audits:**
  - `POST /audits/` (create)
  - `GET /audits/`, `GET /audits/{id}`, `GET /audits/{id}/versions`
- **Workflows:**
  - `POST /workflows/` (create)
  - `GET /workflows/`, `GET /workflows/{id}`
- **Reports:**
  - `POST /reports/export/{audit_id}`
  - `GET /reports/download/{report_id}`
- **Includes all Viewer privileges.**

### Viewer
- **Audits:**
  - `GET /audits/`, `GET /audits/{id}`, `GET /audits/{id}/versions`
- **Workflows:**
  - `GET /workflows/`, `GET /workflows/{id}`
- **Reports:**
  - `GET /reports/download/{report_id}`
- *Cannot create audits, workflows, or request new exports.*

## 6. Proposed Enforcement Architecture
The proposed architecture should overhaul the `require_role` dependency.
Instead of checking a static `User` object, `require_role` should interact with `get_current_org` and verify the user's role against a defined Role Hierarchy.

**Role Hierarchy:**
`owner` > `admin` > `member` > `viewer`

**Implementation details:**
1. Update `OrgRole` enum (after DB migration) to include all four roles.
2. Define a role hierarchy dictionary mapping roles to an integer weight or maintaining a list of allowed roles.
3. Update `backend/dependencies.py` to create a `require_role(min_required_role: str)` factory:
   - This dependency will require `current_user` and `db`.
   - It will query `OrgMember` where `user_id == current_user.id` and `org_id == current_org.id`.
   - It will evaluate if the retrieved `OrgMember.role` has a weight `>=` the `min_required_role`.
   - If `False`, raise `HTTPException(403, "Insufficient permissions")`.
4. Refactor `get_current_org` if necessary:
   - Currently, it relies on returning *any* organization the user is part of. For a multi-org future, `get_current_org` should ideally accept an `X-Organization-ID` header, or the `require_role` dependency should resolve the specific organization context from the request context. However, for now, if a user is strictly limited to 1 org, the current `get_current_org` suffices, but `require_role` still must check the `OrgMember.role` for that specific org.

## 7. Migration Risks
1. **Changing `require_role` Behavior:** The moment `require_role("admin")` goes live, existing users who were assigned the `member` role during registration/testing will lose access to the invite/member endpoints. This is intentional but may break tests or existing workflows if users were improperly categorized.
2. **Endpoint Breakages:** If `require_role` is improperly bound to endpoints where the org context is absent, the dependency graph might fail.
3. **Database Schema Locking:** During the `OrgRole` enum migration, any pending transactions to `organizations` or `org_members` could be blocked or fail depending on SQLite/Postgres enum handling.
