# TarkaX Public Platform Implementation Plan

## Overview
This document outlines the strategic, design, and technical implementation plan for transforming TarkaX from an internal productivity dashboard into an **Organizational Failure Intelligence Platform** designed to generate trust, assessments, reports, and consulting conversations.

---

## PART 1: WEBSITE INFORMATION ARCHITECTURE

### MVP Scope (Build Now)

#### 1. Home
*   **Purpose:** Introduce TarkaX, state the problem (why organizations fail), explain the methodology, and drive users to start an assessment.
*   **Primary CTA:** Start Assessment (Choose AI Audit or Workflow Diagnostic)
*   **Secondary CTA:** Book a Consultation
*   **Key Content Blocks:** Hero (Positioning), Problem Statement, Why Organizations Fail, How TarkaX Works, What TarkaX Detects, Assessment Types, Example Insights, Methodology, Trust Indicators.

#### 2. About TarkaX
*   **Purpose:** Explain the mission and vision behind TarkaX. Frame the company as an intelligence organization preventing operational failures.
*   **Primary CTA:** Book a Consultation
*   **Secondary CTA:** View Methodology
*   **Key Content Blocks:** Our Story, The Cost of Inaction, Leadership/Team (Optional for MVP), Core Principles.

#### 3. AI Audit
*   **Purpose:** Dedicated landing page for the AI Audit assessment. Explain what it is, who it's for, and the value of the output.
*   **Primary CTA:** Start AI Audit
*   **Secondary CTA:** View Sample Report
*   **Key Content Blocks:** What the Audit Covers (Awareness, Adoption, Integration, Governance), Target Audience (e.g., Executives, IT Leaders), Expected Outcomes.

#### 4. Workflow Diagnostic
*   **Purpose:** Dedicated landing page for the Workflow Diagnostic assessment.
*   **Primary CTA:** Start Workflow Diagnostic
*   **Secondary CTA:** View Sample Report
*   **Key Content Blocks:** Identifying Process Friction, Target Audience (e.g., COOs, Department Heads), Expected Outcomes (Automation Blueprints).

#### 5. Methodology
*   **Purpose:** Deep dive into how TarkaX detects failure and generates insights. Build credibility.
*   **Primary CTA:** Start Assessment
*   **Secondary CTA:** Contact Us
*   **Key Content Blocks:** The TarkaX Organizational Health Model (TOHM), Capability Gap Engine, Contradiction Engine, Risk & Forecasting Framework.

#### 6. Trust & Privacy
*   **Purpose:** Establish security and data handling policies to reassure enterprise users.
*   **Primary CTA:** Read Full Privacy Policy
*   **Key Content Blocks:** Data Handling, Stateless Execution (MVP scope), Security Measures, Compliance.

#### 7. Contact
*   **Purpose:** Direct line for enterprise inquiries or general questions.
*   **Primary CTA:** Submit Form / Book Call
*   **Key Content Blocks:** Contact Form, Direct Email, Office Locations (if applicable).

#### 8. Report Delivery (System Page)
*   **Purpose:** The interactive web report presented immediately after assessment completion.
*   **Primary CTA:** Book Consultation
*   **Secondary CTA:** Download PDF
*   **Key Content Blocks:** What is wrong, Why is it wrong, What risk does it create, What should we do next.

### Future Scope (Build Later)
*   Resources (Content Marketing)
*   Benchmark Insights (Data from aggregated anonymized assessments)
*   Research (Whitepapers, Deep Dives)

---

## PART 2: HOMEPAGE DESIGN

### 1. Hero
*   **Headline:** Stop Managing Tools. Start Preventing Organizational Failure.
*   **Subheadline:** TarkaX is an intelligence platform that detects capability gaps, governance friction, and execution risks before they become financial or strategic failures.
*   **CTA:** Diagnose Your Organization (Dropdown to choose assessment)

### 2. Problem Statement
*   **Messaging:** Organizations do not fail because they lack tools. They fail because of Capability Gaps, Governance Gaps, Workflow Friction, Misalignment, and Poor Execution.

### 3. Why Organizations Fail
*   **Visuals:** A clear breakdown of the 5 key failure modes.
*   **Content:** Short, punchy descriptions of how these failures manifest in reality (e.g., "Shadow AI adoption bypassing security protocols").

### 4. How TarkaX Works
*   **Step-by-step Flow:**
    1. Assess (Frictionless entry)
    2. Diagnose (Instant Intelligence Engine processing)
    3. Expose Risk (Identify the gap)
    4. Provide Strategy (Actionable interventions)

### 5. What TarkaX Detects
*   **Grid/List:**
    *   Hidden Capability Gaps
    *   Cross-Functional Misalignment
    *   Compliance & Governance Risks
    *   Process Inefficiencies

### 6. Assessment Types
*   **Cards:**
    *   **AI Audit:** Evaluate AI readiness, adoption, and governance.
    *   **Workflow Diagnostic:** Map process friction and identify automation opportunities.

### 7. Example Insights
*   **Format:** "Consulting-grade" narrative excerpts. Not generic charts, but real sentences: "Risk identified: Marketing department shows high AI adoption but zero governance compliance, creating critical data exposure."

### 8. Methodology
*   **Brief Overview:** Highlighting the deterministic engines (Contradiction, Root Cause, Action Plan) rather than black-box AI.

### 9. Trust Indicators
*   **Content:** "Data is analyzed statelessly. We don't train models on your responses." Emphasize security and enterprise-readiness.

### 10. Call To Action
*   **Closing Block:** "Don't wait for the post-mortem. Diagnose your operational health today."
*   **Buttons:** Start Assessment | Speak with an Expert

---

## PART 3: POSITIONING

**Current Positioning:** Organizational Failure Intelligence Platform

**Why TarkaX is different:**
*   **vs. Consulting firms:** TarkaX provides instant, scalable diagnosis without a 6-week engagement and massive retainer. The assessment *leads* to the high-value consulting conversation.
*   **vs. Surveys:** Surveys collect opinions. TarkaX uses deterministic engines to detect contradictions and capability gaps, transforming input into structural failure analysis.
*   **vs. AI readiness assessments:** Basic assessments give a "score" (e.g., 7/10). TarkaX identifies *why* you are failing (e.g., adoption outpaces governance) and provides a sequenced action plan.
*   **vs. Workflow tools:** Workflow tools manage tasks. TarkaX diagnoses *whether the workflow itself is fundamentally broken or misaligned* with strategy.
*   **vs. Dashboards:** Dashboards show what happened (lagging indicators). TarkaX intelligence engines forecast *what will fail next* and tell you what decision to make.

---

## PART 4: ASSESSMENT ENTRY FLOW

**Goal:** Frictionless lead generation. No account required.

**The User Journey:**
1.  **Landing Page:** User clicks "Start Assessment".
2.  **Choose Assessment:** User selects "AI Audit" or "Workflow Diagnostic".
3.  **Complete Assessment:** User answers questions (using the existing, but streamlined, React forms).
4.  **Email Capture Gate:** A simple modal or step: "Enter your email to instantly view your custom intelligence report."
5.  **View Report:** Instant transition to the interactive Web Report page.
6.  **Receive Report via Email:** Background process sends an email with a link to the report (or PDF) for retention.
7.  **Book Consultation:** Persistent CTAs on the report to "Discuss these findings with an expert" (Calendly integration).

---

## PART 5: REPORT EXPERIENCE

**Goal:** Drive decisions, not data visualization.

**Structure:**
1.  **Executive Summary:** High-level narrative of the organization's health.
2.  **What is wrong? (The Findings):** Clear identification of capability gaps, contradictions, and failure patterns.
3.  **Why is it wrong? (Root Cause):** The underlying structural or strategic reason for the failure.
4.  **What risk does it create? (Risk & Impact):** The forecasted cost of inaction (financial, operational, strategic).
5.  **What should we do next? (Action Plan):** Sequenced, role-based recommendations (Immediate, 30-Day, 90-Day).
6.  **Consulting CTA:** "Need help executing this plan? Book a Strategy Workshop."

---

## PART 6: CONSULTING CONVERSION FLOW

**Goal:** Fastest path to a conversation using MVP tools.

**Transition Flow:**
1.  **Trigger:** User reads the Web Report and realizes the severity of the findings.
2.  **CTA Placement:** Persistent button on the Web Report header and a dedicated block at the end of the Action Plan section.
3.  **Action:** User clicks "Book Consultation" or "Request Workshop".
4.  **Mechanism (MVP):** Direct link to a Calendly booking page (or a simple React form that sends an email to the TarkaX team). No custom scheduling infrastructure built in-house.

---

## PART 7: TRUST CENTER

**Goal:** Feel closer to Gartner or McKinsey than a startup tool.

**Key Components (to be built into the "Methodology" and "Trust & Privacy" pages):**
*   **Assessment Methodology:** Explanation of the deterministic engines (Layer 1 to Layer 5.5).
*   **Evidence Framework:** How inputs are validated (even if manual for MVP).
*   **Confidence Index:** How TarkaX adjusts risk scores based on data quality.
*   **Privacy & Data Handling:** Clear statements on stateless execution, lack of LLM training on user data, and GDPR/CCPA compliance basics.
*   **Benchmarking Approach (Teaser):** Explain that insights are evaluated against industry baselines (even if fully implemented in V2).

---

## PART 8: TECHNICAL IMPLEMENTATION (FRONTEND AUDIT)

### Current State Audit

*   **`LandingPage.tsx`**: **REPLACE**. Current page is a "dark cinematic" dashboard pitch ("Strategic Systems Optimization"). Needs complete replacement to match the "Organizational Failure Intelligence" positioning.
*   **`App.tsx`**: **WORKING (Needs Update)**. Needs new public routes added outside the `<PrivateRoute>` wrapper.
*   **`NewAudit.tsx`**: **WORKING (Needs Refactor)**. Currently behind authentication. Must be moved to a public route and appended with the Email Capture step.
*   **`NewWorkflow.tsx`**: **WORKING (Needs Refactor)**. Currently behind authentication. Must be moved to a public route and appended with the Email Capture step.
*   **`AuditDetail.tsx`**: **WORKING (Needs Refactor)**. Currently designed as an internal dashboard view with "Radar Charts" and scores. Needs a complete redesign to match the narrative "What is wrong / Why / Risk / Next Steps" Web Report format. Must support public access via token/ID.
*   **`Dashboard.tsx`**: **WORKING (Internal)**. This remains the internal view for consultants/admins, but is no longer the main user flow.
*   **Authentication Flow (`Login.tsx`, `Register.tsx`, `PrivateRoute.tsx`)**: **WORKING**. Leave as-is for internal admin/consultant access. Do not modify for the public flow.

### Required Changes (Application Layer Only)

1.  **New Routes (Public):**
    *   `/` -> New `Home.tsx`
    *   `/about` -> New `About.tsx`
    *   `/assessments/ai-audit` -> Modified `NewAudit.tsx` (Public version)
    *   `/assessments/workflow` -> Modified `NewWorkflow.tsx` (Public version)
    *   `/methodology` -> New `Methodology.tsx`
    *   `/trust` -> New `TrustCenter.tsx`
    *   `/report/:id` -> New `WebReport.tsx` (Public, unauthenticated view of the results)

2.  **Modified Components:**
    *   Create a public `Layout.tsx` (Header with Nav, Footer) distinct from the internal `AppShell.tsx`.
    *   Modify Assessment forms to end with an `EmailCaptureModal.tsx` instead of redirecting to the internal dashboard.

3.  **API/Backend Implications (Minimal):**
    *   Endpoints for submitting assessments must accept unauthenticated POST requests (or use a public API key).
    *   A new endpoint to associate an email with an assessment ID *after* completion.
    *   Ensure the GET endpoint for fetching a report by ID does not require a JWT, provided the ID is sufficiently complex/unguessable (UUIDv4).

---

## PART 9: MVP VS FUTURE

### Build Now (MVP)
*   New Marketing Pages (Home, About, Methodology, Trust).
*   Public routing for assessments without authentication.
*   Email capture step at the end of the assessment.
*   Narrative-first Web Report experience (`WebReport.tsx`).
*   Calendly integration for Consulting Conversion.

### Build Later
*   Resources, Benchmark Insights, Research pages.
*   Collaborative assessment mode (multiple users answering one assessment).
*   User accounts for historical tracking.
*   PDF Export (if the Web Report is sufficient for MVP, PDF can be deferred, though backend code exists for it).

### Do Not Build Yet
*   Custom scheduling infrastructure.
*   CRM capabilities within TarkaX.
*   Deep integration tracking (Jira, Asana).
*   LLM-based unstructured evidence parsing (stick to deterministic forms).
