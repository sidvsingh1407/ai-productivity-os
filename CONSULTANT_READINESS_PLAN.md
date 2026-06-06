# Sprint: Consultant Readiness Implementation Plan

## Executive Summary
Based on the Product Gap Analysis, the highest-value path to revenue is ensuring TarkaX serves its primary target audience: Independent and Boutique Consultants. To capture this market, the platform must support multi-user collaboration (consultant + client), generate boardroom-ready deliverables, and prove its methodology.

This sprint pivots away from internal auditability (logs) and focuses entirely on Consultant Readiness.

---

## WORKSTREAM A: RBAC & Organization Collaboration

### Current State
* Organizations and Users exist in the database.
* Registration automatically creates an organization.
* The API dependency `require_role` is a stub that returns the current user without verifying organizational roles.
* No UI exists for inviting team members, assigning roles, or switching contexts.

### Missing Capability
* **Backend RBAC Enforcement:** `require_role` must validate the user's specific `OrgRole` (Owner, Admin, Member, Viewer) against the `ROLE_HIERARCHY` within their active organization context.
* **Invitation Lifecycle:** APIs and UI to generate, send, and accept invitations with assigned roles.
* **Organization Management UI:** A dashboard for Owners/Admins to view, invite, and remove team members.

### User Value
Consultants can securely invite clients as 'Viewers' to see read-only results, or invite junior analysts as 'Members' to run assessments, without sharing login credentials.

### Revenue Impact
**High.** B2B sales require seat management. It allows TarkaX to eventually charge per-seat or per-workspace, rather than per-individual. It removes a critical enterprise blocker.

### Files Affected
* `backend/dependencies.py` (Implement `require_role` logic)
* `backend/organizations/router.py` (Invitation/Acceptance endpoints)
* `backend/organizations/service.py` (Invitation logic)
* `backend/models/organization.py` (Update schemas if necessary)
* `frontend/src/pages/Settings/OrgSettings.tsx` (Add member management UI)
* `frontend/src/components/admin/*` (Member table components)

### Risk Level
**High.** Modifying auth dependencies and role hierarchies can inadvertently lock users out or expose cross-tenant data if not rigorously tested.

---

## WORKSTREAM B: Executive PDF Deliverables

### Current State
* The backend generates a PDF via `ReportLab` (`backend/reports/pdf_generator.py`).
* The PDF output is a functional data dump, lacking consulting-grade styling, structure, and executive narrative flow.

### Missing Capability
* **Consultant-Grade Structure:** The PDF must follow a strict narrative: Executive Summary -> Risk Projection -> Findings -> Recommendations -> Roadmap.
* **Boardroom Styling:** Clean, professional layouts using ReportLab components (tables, spacers, structured headers) that mimic a McKinsey or Gartner brief.
* **Dynamic Intelligence Injection:** The PDF must dynamically consume the unified `intelligence` payload rather than raw scores.

### User Value
Consultants can instantly download a professional report and present it to a client board, saving hours of manual slide deck creation.

### Revenue Impact
**Critical.** The PDF *is* the product for the consultant. High-quality deliverables justify premium pricing ($100+ per assessment run).

### Files Affected
* `backend/reports/pdf_generator.py` (Complete rewrite of layout and data ingestion)
* `backend/tasks/pdf_tasks.py` (Ensure task passes correct payload)
* `backend/verify_pdf.py` (Update verification script)

### Risk Level
**Medium.** ReportLab can be brittle with complex layouts. Keeping the design clean, structural, and text-heavy minimizes generation crashes.

---

## WORKSTREAM C: Explainability & Methodology

### Current State
* The platform generates deterministic findings, but the UI focuses heavily on raw scores.
* Public methodology pages (`/methodology`, `/research`, `/trust`) are placeholders or nonexistent.

### Missing Capability
* **Explainable UI:** The web report must explicitly explain *why* a score was given, showing the rules triggered and the Confidence Index.
* **Methodology Hub:** Publicly accessible documentation explaining the 5-dimension TOHM framework, ensuring buyers trust the science behind the tool.

### User Value
Builds immediate trust. Users understand they are buying a rigorous intelligence engine, not a generic LLM wrapper.

### Revenue Impact
**High.** Trust accelerates the enterprise sales cycle. Consultants can point to the TarkaX methodology to validate their own advisory services.

### Files Affected
* `frontend/src/pages/marketing/MethodologyPage.tsx` (New)
* `frontend/src/pages/marketing/TrustPage.tsx` (New)
* `frontend/src/components/layout/Navbar.tsx` & `Footer.tsx` (Navigation updates)
* `frontend/src/pages/AuditDetail.tsx` (Add "Why This Score?" contextual UI)

### Risk Level
**Low.** Primarily frontend UI and content addition.

---

## Recommended Implementation Order

1. **Workstream B (Executive PDF Deliverables):** Fix the core value proposition immediately. Ensure the primary artifact is ready for sale.
2. **Workstream A (RBAC & Collaboration):** Secure the platform and enable the team-based usage required by consulting firms.
3. **Workstream C (Explainability & Methodology):** Polish the public framing to drive inbound trust and conversion.
