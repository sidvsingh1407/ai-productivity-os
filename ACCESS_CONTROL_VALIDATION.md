# Access Control Validation

This document verifies the access control enforcement mechanisms within the TarkaX backend and how they behave for both anonymous and authenticated users.

## Expected Behavior: Anonymous Users
Anonymous users do not have a valid JWT token.
- Attempting to access protected endpoints (e.g., `/audits`, `/reports`, `/organizations`, `/users/me`) will result in a FastAPI `HTTPException(401, "Could not validate credentials")` because the `get_current_user` dependency will fail to decode a token or find an associated user.
- **Result:** Anonymous users **cannot** read audits, reports, organizations, or user records.

## Expected Behavior: Authenticated Users
Authenticated users provide a valid JWT token.
- `get_current_user` extracts the user ID and successfully fetches the user record.
- `get_current_org` ensures the user has a valid mapping in `org_members`.
- Endpoints and repository methods explicitly scope their database queries using the users `org_id`. For example:
  - `select(Audit).where(Audit.org_id == org_id)`
  - `select(Organization).where(Organization.id == org_id)`
- **Result:** Authenticated users **can only access** records belonging to their assigned organization. Cross-tenant access is programmatically impossible via the API layer.

## Automated Verification Tests
We have added automated tests to verify these access control rules. The tests simulate anonymous and authenticated requests to ensure the FastAPI dependency injection correctly blocks or scopes access.
