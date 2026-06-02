# P1 ONBOARDING BLUEPRINT: First-Time User Experience (FTUX)

## 1. UX Architecture

**Core Philosophy:** Inline dashboard onboarding. No mandatory modals, wizards, or forced tutorials. The dashboard itself transforms into the activation layer for first-time users.

**Success Metric:** Maximize First Audit Completion Rate.
**Goal:** Within 30 seconds, a user must understand:
1. What AI Productivity OS is.
2. What an AI Audit does.
3. What they will receive (the outcome).
4. How long it takes.
5. What to click first.

### State Routing Logic
- **State 0 (First Login - 0 Audits, 0 Workflows):** Show the Onboarding Dashboard (Empty State with Activation Checklist & Explanations).
- **State 1 (Audit in Progress):** Show progress indicators, maintaining anticipation of the outcome.
- **State 2 (First Audit Completed - Success State):** Show the Success Dashboard (Score, Rating, Key Insights, Next Actions).
- **State 3 (Return User - Has Data):** Standard Operational Dashboard (Analytics, History).

---

## 2. Wireframe-Level Layouts

### A. First Login Dashboard (The Onboarding State)

```text
================================================================================
Header: Welcome, [Name]. Let's baseline your AI operations.
Sub-header: AI Productivity OS helps you measure, secure, and optimize your
organization's AI adoption.
================================================================================

[ Hero Section: The Value Proposition & Primary CTA ]
--------------------------------------------------------------------------------
|  What is an AI Audit?                                                        |
|  A 5-minute assessment that measures how safely and effectively your team    |
|  uses AI.                                                                    |
|                                                                              |
|  What you'll get:                                                            |
|  • An overall maturity score                                                 |
|  • Key strengths and identified risks                                        |
|  • Recommended next actions to improve                                       |
|                                                                              |
|  [ Primary Button: Run First AI Audit ]  (Time: ~5 mins)                     |
|  [ Secondary Button: View Example Audit ]                                    |
--------------------------------------------------------------------------------

[ Onboarding Checklist Section ]
--------------------------------------------------------------------------------
|  Getting Started                                                             |
|  [ ] Run your first AI Audit                                                 |
|  [ ] Review your maturity score                                              |
|  [ ] Explore recommendations                                                 |
--------------------------------------------------------------------------------

[ Contextual Education Layer (Cards) ]
--------------------------------------------------------------------------------
| Card 1: AI Audit                  | Card 2: Workflow Diagnostic              |
| -----------------                 | -----------------------                  |
| Measures your baseline maturity   | Evaluates specific team processes to     |
| and governance. Starts here.      | find AI automation opportunities.        |
| (Uses: Organizational Health)     | (Uses: Process Optimization)             |
--------------------------------------------------------------------------------
```

### B. Success Experience Dashboard (Post-First Audit)

```text
================================================================================
Header: Assessment Complete. Here is your baseline.
================================================================================

[ Top Highlights ]
--------------------------------------------------------------------------------
|  Score: 68/100  |  Rating: Developing  |  Risk Level: Moderate               |
--------------------------------------------------------------------------------

[ Key Insights & Next Actions ]
--------------------------------------------------------------------------------
|  Top Strength: High employee enthusiasm for AI tools.                        |
|  Top Risk: Lack of formal data privacy guidelines.                           |
|                                                                              |
|  Next Recommended Action:                                                    |
|  Review your detailed report to implement governance frameworks.             |
|                                                                              |
|  [ Button: View Full Audit Report ]                                          |
--------------------------------------------------------------------------------

[ Onboarding Checklist Section ]
--------------------------------------------------------------------------------
|  Getting Started                                                             |
|  [x] Run your first AI Audit                                                 |
|  [x] Review your maturity score                                              |
|  [ ] Explore recommendations (Pending)                                       |
--------------------------------------------------------------------------------
```

---

## 3. Component List

1. **`OnboardingDashboard`:** The main layout component for users with zero data.
2. **`ValueHero`:** Explains the "What," "Why," and "Time expected" with primary CTA.
3. **`GettingStartedChecklist`:** A dynamic component reading completion state (Audit count > 0).
4. **`FeatureExplanationCards`:** Lightweight cards defining "AI Audit" vs "Workflow Diagnostic" without jargon.
5. **`DemoAuditModal` / `DemoAuditViewer`:** A dedicated read-only view of a "Sample Audit" that overlays or routes without saving to the DB.
6. **`SuccessDashboard`:** The transitional dashboard shown immediately after the first audit is completed, emphasizing "What to do next."
7. **`ContextualTooltip`:** Reusable UI wrapper for adding info icons explaining terms like "Governance," "Score," or "Risk."

---

## 4. User Journey (Before vs. After)

### Before (Current State)
1. User registers and logs in.
2. Lands on `Dashboard.tsx`.
3. Sees 0 "Total Audits", 0 "Last Score", and "Pending" compliance.
4. Confused about what the platform actually does.
5. Sees two buttons ("Run AI Audit", "Run Workflow Diagnostic") with no context on the difference or time required.
6. **Result:** High risk of drop-off; low activation.

### After (P1 State)
1. User registers and logs in.
2. Lands on `Dashboard.tsx` (which detects 0 audits).
3. Sees a clear, executive summary of what AI Productivity OS is.
4. Reads exactly what an AI Audit is, what they will get, and that it takes 5 minutes.
5. Clicks "View Example Audit" to see a risk-free sample outcome.
6. Feels confident and clicks "Run First AI Audit".
7. Completes the audit, lands on the `SuccessDashboard`, sees their score, and is guided to read the full report.
8. **Result:** Clear comprehension, high activation, zero confusion.

---

## 5. Recommended Copy (Executive + Practical + Encouraging)

**Headline:** Welcome, [Name]. Let's baseline your AI operations.
**Sub-headline:** AI Productivity OS helps you measure, secure, and optimize your organization's AI adoption.

**The "What & Why" (Hero):**
> **Run an AI Audit to understand how effectively your organization is adopting AI.**
> In about 5 minutes, you'll receive an overall score, identified risks, and practical next steps to improve your operations.

**Buttons:**
> Primary: **Run First AI Audit** *(Takes ~5 mins)*
> Secondary: **View Sample Report**

**Checklist:**
> **Getting Started**
> [ ] Complete first AI Audit
> [ ] Review your baseline score
> [ ] Explore practical recommendations

**Feature Explanations:**
> **AI Audit:** A high-level assessment of your organization's AI readiness, security, and usage.
> **Workflow Diagnostic:** A deep dive into a specific team process to find where AI can save time.

**Contextual Help (Tooltips):**
> *Governance:* The rules and policies your company uses to keep data safe when using AI.
> *Maturity Score:* A benchmark from 0-100 indicating how advanced and secure your AI practices are.

---

## 6. Priority Ranking (Execution Order)

1. **Dashboard Routing Logic:** Implement detection for first-time users (e.g., `totalAudits === 0`).
2. **Onboarding Dashboard UI:** Build the `ValueHero`, `GettingStartedChecklist`, and `FeatureExplanationCards`.
3. **Demo Experience (Sample Report):** Create the static read-only "Sample Audit" viewer.
4. **Success Experience UI:** Build the state for exactly 1 completed audit (celebration + next actions).
5. **Contextual Help:** Add lightweight tooltips to key terms across the dashboard and audit forms.

---

## 7. Exact Files To Modify

* **`frontend/src/pages/Dashboard.tsx`**
  - Refactor to handle the three states (Onboarding, Success, Standard).
* **`frontend/src/components/ui/` (New & Existing)**
  - Add `ContextualTooltip.tsx` (using Shadcn/ui or existing tooltip patterns).
* **`frontend/src/components/dashboard/` (New Folder)**
  - Create `OnboardingHero.tsx`
  - Create `GettingStartedChecklist.tsx`
  - Create `FeatureExplanations.tsx`
  - Create `SuccessHighlights.tsx`
* **`frontend/src/pages/SampleAudit.tsx` (New File)**
  - Create the read-only, pristine demo experience, accessible via a new route or modal overlay.
* **`frontend/src/App.tsx` / Routing logic**
  - Register the `/sample-audit` route.

---

## 8. Estimated Effort

* **UX/State Logic Updates:** 1-2 hours (Querying backend/store for audit count and routing state).
* **Component Implementation (Hero, Checklist, Cards):** 3-4 hours.
* **Sample Audit (Demo) Page Construction:** 2-3 hours (Building a static version of the AuditDetail page with hardcoded data).
* **Success State Design & Wiring:** 2 hours.
* **Review & Polish (Tooltips, Copy, Responsive Design):** 2 hours.
* **Total Estimated Time:** ~10-13 hours for full P1 FTUX implementation.
