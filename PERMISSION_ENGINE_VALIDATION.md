# Permission Engine Security Validation Evidence

## Scope
Tested the newly implemented `require_role()` dependency mapping against FastAPI routing logic. Validation covers:
1. Cross-organization access prevention.
2. Role hierarchy enforcement (Viewer vs. Member).

## 1. Cross-Organization Access (Data Isolation)
**Test Scenario:**
- User A belongs to Organization A.
- User B belongs to Organization B.
- User A requests Audit ID belonging to Organization B.

**Result:** `GET /audits/{audit_org_b.id}` returns `404 Not Found` (Repository level) or `403 Forbidden` (Dependency level if extended). In this codebase, the repository correctly scopes queries by `org_id`, returning `404`.

**Output:**
```
Test DB setup complete.
Request: GET /audits/c7839138-dc69-4940-8243-5a8114d987e1
Response Status: 404
Security validation passed: User A cannot access Org B audits.
```

## 2. Role Hierarchy Enforcement
**Test Scenario:**
- User V is assigned the `viewer` role in Organization Test.
- User V attempts to read audits via `GET /audits/` (Requires `viewer` role or higher).
- User V attempts to create an audit via `POST /audits/` (Requires `member` role or higher).

**Result:**
- `GET /audits/` returns `200 OK` (Viewer authorized).
- `POST /audits/` returns `403 Forbidden` (Viewer unauthorized).

**Output:**
```
Viewer GET /audits/: 200
Viewer POST /audits/: 403
Security validation passed: Hierarchy enforced via dependency.
```

## Conclusion
The backend now properly enforces role hierarchy mapping (`owner` > `admin` > `member` > `viewer`) and uses the `OrgMember` mapping table to resolve permissions dynamically on a per-request basis. Unauthorized access attempts correctly yield `403 Forbidden`. Cross-organization access maintains `404 Not Found` data isolation limits.
