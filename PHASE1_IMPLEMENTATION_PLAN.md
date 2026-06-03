# TarkaX Phase 1 — Product Stabilization Sprint Implementation Plan

## Executive Summary

* **Current readiness assessment:** The application has a strong foundational UI and conceptual architecture. However, several core user journeys (AI Audit generation, PDF Exports, Contact capture) are blocked by missing or disconnected backend logic. The platform is currently not ready for a live demo.
* **Key launch blockers:**
  * AI Audit generation lacks a deterministic scoring backend, preventing end-to-end report creation.
  * PDF Export endpoints and tasks are present but the PDF generation is fundamentally unlinked or failing because of missing integrations in standard paths, and the file download flow is unverified.
  * Contact form has no persistence layer, leading to silent lead failures.
  * Legal pages (`/privacy` and `/terms`) are missing.
  * Numerous dead links (`to="#"`) exist across marketing and blog pages.
* **Estimated Phase 1 scope:** Focus entirely on stabilizing the MVP core (Audit -> PDF -> Lead Capture). All advanced functionality (Forecasting, Benchmarking) will be routed to the contact form to preserve roadmap intent while ensuring a flawless current-state UX.

---

## Workstream A — AI Audit

**Issue:** User cannot complete an AI audit and receive a reliable, believable result because the scoring engine requires a deterministic fallback and the frontend flow needs to handle real data.
* **Problem:** Audit results page (`AuditDetail.tsx`) relies on a missing or incomplete backend deterministic engine to generate the overall score, dimensions, findings, and recommendations.
* **Root Cause:** Backend `scoring_engine.py` is partially implemented but missing deterministic mock generation for findings and recommendations in the main audit processing flow.
* **Proposed Fix:** Enhance `backend/audits/scoring_engine.py` and `backend/audits/service.py` to generate deterministic findings, recommendations, and missing data flags based on the calculated dimension scores. Update `AuditDetail.tsx` to ensure it gracefully renders these values.
* **Files Affected:** `backend/audits/scoring_engine.py`, `backend/audits/service.py`, `backend/models/audit.py`, `frontend/src/pages/AuditDetail.tsx`
* **Risk Level:** Medium. Changing the scoring engine output structure could break the frontend expectations if not mapped perfectly.
* **Estimated Effort:** 2 hours.

---

## Workstream B — PDF Export

**Issue:** PDF Export functionality is broken or incomplete.
* **Current Implementation:** Backend contains `pdf_generator.py` (ReportLab) and a Celery task `pdf_tasks.py`. `reports/router.py` exists but its integration with the actual download flow and `ReportLab` needs verification.
* **Failure Point:** Backend references `IntegrationResult` inside `pdf_tasks.py` which may not exist, and the Celery task runner might not be active, meaning async PDF generation hangs or fails silently. `pdf_generator.py` relies on hardcoded payload structures that may not match `scoring_engine.py` outputs.
* **Proposed Architecture:** Use `ReportLab` to build the PDF. To avoid Celery/async complexities in the stabilization sprint, we will make PDF generation a synchronous task on the export endpoint (or ensure the async flow does not require an external Celery worker if possible, or trigger it directly). We will ensure `pdf_generator.py` creates a standard consulting report using the deterministic AI Audit data.
* **Files Affected:** `backend/reports/pdf_generator.py`, `backend/reports/router.py`, `backend/tasks/pdf_tasks.py`, `backend/reports/service.py`
* **ReportLab integration plan:** Ensure `generate_audit_pdf` produces a beautiful, text-heavy consulting deliverable mapping to the 5 dimensions, critical findings, and recommendations.

---

## Workstream C — Contact Form

**Issue:** Lead capture may not function and has no persistence.
* **Frontend changes:** Update `ContactPage.tsx` to submit data via Axios/`apiClient` to a new backend endpoint. Add success and error states to the UI.
* **Backend endpoint:** Create `POST /api/leads` (e.g., in a new or existing router like `organizations/router.py` or a dedicated `leads/router.py`).
* **Database schema:** Create `contact_leads` table (`id`, `name`, `email`, `company`, `message`, `source_page`, `created_at`) via a new SQLAlchemy model.
* **Lead storage flow:** `ContactPage.tsx` -> `POST /leads` -> Validation (Pydantic) -> Insert to `contact_leads` -> Return `201 Created`.
* **Validation strategy:** Pydantic schema enforcing email format and required fields (Name, Email, Interest).
* **Files Affected:** `backend/models/organization.py` (or new `lead.py`), `backend/main.py`, `frontend/src/pages/marketing/ContactPage.tsx`.

---

## Workstream D — Frontend Stability

**Issue:** Ensure the frontend builds cleanly and navigates without failure.
* **Missing dependencies:** The build step completed successfully (`npm run build`), but we will verify all runtime dependencies.
* **Build failures:** Currently passing, but we must ensure strict TypeScript checks don't fail when integrating new APIs.
* **TypeScript issues:** Ensure strict typing for new Lead capture and Audit responses.
* **Routing issues:** Ensure all valid routes are covered in `App.tsx` and public marketing routes don't enforce auth incorrectly.
* **Import issues:** Verify absolute vs relative paths in components.
* **Priority:** Fix typing errors first, then route boundaries.

---

## Workstream E — Legal & Trust

**Issue:** Missing standard legal pages.
* **Privacy Policy:** Create `frontend/src/pages/marketing/PrivacyPage.tsx`. Content tailored to TarkaX (data privacy for organizational audits, uploaded info, report generation).
* **Terms of Service:** Create `frontend/src/pages/marketing/TermsPage.tsx`. Content tailored to TarkaX (user accounts, acceptable use, consulting deliverables).
* **Routes:** Add `/privacy` and `/terms` to `App.tsx`.
* **Footer updates:** Link these pages in the global footer.
* **Files Affected:** `frontend/src/pages/marketing/PrivacyPage.tsx`, `frontend/src/pages/marketing/TermsPage.tsx`, `frontend/src/App.tsx`, `frontend/src/components/layout/MarketingLayout.tsx`.

---

## Workstream F — Navigation & Broken Links

**Issue:** Dead links (`to="#"`) exist across the app.

| Route/Button | Current Behavior | Proposed Behavior |
| --- | --- | --- |
| `MarketingLayout.tsx` (Mobile Menu) | `to="#"` | Route to `/contact?interest=General+Inquiry` or specific pages |
| `AboutPage.tsx` (Careers/Investors) | `to="#"` | Route to `/contact?interest=Partnerships` |
| `BlogPage.tsx` (Article Cards) | `to="#"` | Route to `/contact?interest=Content+Subscription` or hide if articles aren't ready |
| `Home.tsx` / Nav (Forecasting) | Potential Dead Links | Route to `/contact?interest=Forecasting+Framework` |
| `Home.tsx` / Nav (Benchmarking) | Potential Dead Links | Route to `/contact?interest=Benchmarking` |

* **Rule enforced:** Every button must navigate, execute an action, or communicate unavailability (via `/contact` redirect).

---

## Forecasting Recommendation

**Question:** Should Forecasting remain A. Standalone Product or B. Risk Projection Layer?

**Recommendation:** **B. Risk Projection Layer** inside AI Audit and Workflow Diagnostic.

**Reasoning:**
1. **Contextual Relevance:** Forecasting is most powerful when it builds upon an established baseline. Presenting it as an isolated product forces the user to provide context twice. Embedding it as a layer within the AI Audit naturally extends the value of the audit (e.g., "Here is your current score, and here is your projected risk if no action is taken").
2. **Phase 1 Constraints:** We lack the longitudinal data and complex ML pipelines (TimesFM) required for a true standalone forecasting product right now. A "Risk Projection Layer" can be simulated deterministically based on the current AI Audit gaps, making it highly achievable in the near term.
3. **Consulting Utility:** Consultants sell "Cost of Inaction". A risk projection layer natively supports this narrative directly inside the primary deliverable.

---

## Implementation Order

1. **Workstream D — Frontend Stability:** Ensure the foundation is solid before adding features.
2. **Workstream C — Contact Form:** Establish the core lead capture mechanism. We need this ready so out-of-scope links can be redirected here.
3. **Workstream F — Navigation & Broken Links:** Clean up the UX and route dead features to the now-functional contact form.
4. **Workstream E — Legal Pages:** Quick wins to establish trust and complete the site footer.
5. **Workstream A — AI Audit Engine & Results Generation:** Core value prop. Build the deterministic engine so users get real results.
6. **Workstream B — PDF Export:** The final piece. Connect the deterministic audit data to the ReportLab PDF generator.

**Rationale:** We build from the outside in. First, capture leads and stabilize the public shell. Then, fix the core product loop (Audit -> Results). Finally, cap it off with the exportable deliverable (PDF).

---

## Risk Assessment

* **Contact Form (Low):** Standard CRUD operation. Low risk of side effects.
* **Legal Pages / Navigation (Low):** Purely frontend routing and content updates.
* **AI Audit Deterministic Engine (Medium):** Requires careful mapping between the scoring engine output and the frontend `AuditDetail.tsx` expectations. If the data shapes don't match, the results page will crash.
* **PDF Export (High):** The existing PDF architecture relies on Celery tasks and complex `ReportLab` structures. Migrating this to a reliable, synchronous (or easily verifiable) flow without breaking existing imports or hanging the server is the highest risk component of this sprint.

---

## Expected Outcomes

After Phase 1 completes, the user journey will be:

1. **Visitor -> Homepage:** User lands on the site, explores value props, and clicks "Start AI Audit".
2. **AI Audit:** User completes the 5-step diagnostic form. Submission hits the deterministic backend scoring engine.
3. **Results Page:** User is redirected to `/audits/:id` where they instantly view their overall score, dimension breakdown, findings, and recommendations.
4. **PDF Export:** User clicks "Download Report". The backend synchronously generates a professional ReportLab PDF and streams it to the user.
5. **Contact/Lead Capture:** If the user explores out-of-scope features (Forecasting) or wants a demo, they are routed to `/contact`. They submit the form, and their lead is stored securely in the database (`contact_leads`), providing a seamless end-to-end experience with zero broken flows.
