# TarkaX Consultant Platform V1 Architecture
## Organizational Failure Intelligence as a Consulting Operating System

---

## 1. Executive Summary

TarkaX is evolving into an **Organizational Failure Intelligence Platform**, specifically structured as the core operating system for consultants. This platform does not exist merely to display dashboards or capture survey responses. It exists to enable consultants to **win clients, diagnose deep organizational failure, drive interactive workshops, demonstrate progress, and secure renewals**.

By standardizing the intelligence pipeline—from evidence collection to diagnosis, risk mapping, and multi-horizon action planning—TarkaX allows Independent Consultants, Boutique Firms, Enterprise Practices, and Government Advisory Firms to dramatically scale their diagnostic accuracy and client impact.

The fundamental design rule of this architecture is answering: **What decision should the consultant or client be able to make?**

---

## 2. Consultant User Journey

TarkaX supports two operating modes to accommodate different engagement styles and phases. The MVP prioritizes the **Consultant-Led** mode, while architecting for the future **Collaborative** mode.

### Mode A: Consultant-Led (MVP Priority)
The consultant retains full control of the inputs and narrative, acting as the interrogator and diagnostician.
1. **Lead / Win Client:** Consultant uses a public, frictionless TarkaX preview assessment (showing 1 high-value insight: Risk Level, Confidence, Impact) to convert a prospect into a paying client.
2. **Discovery & Assessment:** Consultant interviews the client's executive team and inputs qualitative evidence (text, URLs) directly into TarkaX.
3. **Diagnosis:** TarkaX Engine processes evidence to identify Capability Gaps and Failure Patterns.
4. **Proposal:** Consultant exports a dynamically generated Executive Summary PDF to secure the full consulting engagement.
5. **Workshop:** Consultant runs the **TarkaX Workshop Mode** live with the client leadership to validate root causes and assign action ownership.
6. **Implementation:** Consultant uses the passive tracking board to run 30/60/90-day check-in meetings.
7. **Demonstrate Progress & Renew:** After 6-12 months, consultant runs a Follow-Up Assessment to prove Capability Growth and Risk Reduction, securing a contract renewal or expansion.

### Mode B: Collaborative (Architected for Future)
The consultant distributes the assessment across the client's organization to measure reality gaps and alignment.
1. **Setup:** Consultant defines the client hierarchy and sends role-based invites (Leadership, Managers, Employees).
2. **Assessment:** Client personnel complete the assessments directly. TarkaX scales the evidence burden by role (High for Leadership, Low for Employees) to maximize completion.
3. **Diagnosis:** TarkaX calculates **Reality Gaps** (highest minus lowest score) and **Alignment Gaps** (Leadership vs. Manager vs. Employee).
4. **Workshop to Renewal:** Follows the same path as Mode A, but enriched with organizational friction data.

---

## 3. Consultant Workspace

The Consultant Workspace is the central command center designed around driving engagements forward, not passive data management.

### Capabilities
* **Client Pipeline:** Track leads from initial public assessment preview to signed engagement.
* **Active Engagements:** High-level status of ongoing implementations and upcoming check-ins.
* **Assessment Management:** Hub for launching, tracking, and editing both Consultant-Led and Collaborative assessments.
* **Benchmark Library:** Access internal portfolio trends (L1) and anonymized global TarkaX trends (L2).
* **Report Generation:** Export modular reports targeted at specific audiences (Executive, Manager, Consultant, Government).
* **Follow-Up Tracking:** Alerts for upcoming 30/60/90-day review cycles.

### High-Level Conceptual Data Model
The architecture ensures strict multi-client isolation and supports deep firm structures.
```text
Firm
└── Practice
    └── Consultant
        └── Client
            ├── Engagement
            │   ├── Assessment (Base)
            │   ├── Assessment (Follow-Up)
            │   └── Report Generation
            └── Action Plan (Implementation Tracking)
```

### Permissions
* **Firm Admin:** Global view of all practices, revenue, and cross-portfolio benchmarking.
* **Practice Lead:** View of all consultants and clients within their specialized practice.
* **Consultant:** Isolated view of their assigned clients, assessments, and engagements.

---

## 4. Client Portfolio Management

For consultants managing multiple clients simultaneously, TarkaX provides a macro-view of organizational failure across their portfolio.

### Capabilities
* **Portfolio Overview:** A single pane of glass showing the current risk level of every active client.
* **Cross-Client Benchmarking:** Identifying systemic issues across the consultant's book of business.
* **Risk Monitoring:** Flagging clients where implementation has stalled (identifying churn risk).
* **Renewal Opportunities:** Highlighting clients who are due for a 6-month or 12-month reassessment.

### Portfolio Health Dashboard Outputs
The dashboard emphasizes actionable alerts over raw data. E.g., *"Client X has missed 3 consecutive 30-Day actions; high risk of implementation failure."*

---

## 5. White Label Platform

TarkaX is designed to disappear behind the consulting firm's brand, increasing the perceived value of the consultant's proprietary methodology.

### MVP White Label (Build Now)
Strictly focused on UI and reporting aesthetics.
* **Logo:** Client and Firm logos on dashboards and exported reports.
* **Brand Colors:** Primary and secondary colors applied to the TarkaX UI and PDFs.
* **Report Branding:** Ability to adjust the tone and titling of the dynamic PDF generator.
* **Email Branding:** Firm branding on automated report delivery or Collaborative assessment invites.

### Advanced White Label (Build Later)
* **Custom Domain:** e.g., `assessments.consultingfirm.com`
* **Custom Login Pages:** Fully branded authentication flows.
* **Full Portal:** Removing all TarkaX branding entirely.

---

## 6. Client Benchmarking

Benchmarking answers: *"What should an organization like this reasonably look like?"* It explicitly avoids benchmarking against perfection.

### Level 1: Portfolio Benchmarking (MVP)
Insights derived exclusively from the consultant's or firm's own client base.
* **Consultant View:** *"Across your 14 clients, 62% struggle with Governance and 41% struggle with Tool Sprawl."*
* **Client View:** *"Compared to other clients managed by [Firm Name], your Technology Adoption maturity is in the bottom 20%."*

### Level 2: Global TarkaX Benchmarking (Future)
Insights derived from the anonymized global TarkaX dataset.
* **Consultant View:** Industry-wide macro trends.
* **Client View:** *"Compared to 500 organizations of similar size and industry globally, your Alignment Gap is 30% wider."*
* **Anonymization:** Strict data scrubbing; segmentation by Size, Type, and Industry only.

---

## 7. Workshop Mode

Workshop Mode expressly replaces static slide decks and PDFs. It is a live-navigable, interactive dashboard used by the consultant during leadership meetings to force decisions.

### Features
* **Presentation Mode:** High-contrast, focused UI designed for screen sharing or projector viewing.
* **Executive View:** Level 1 assessment view (What is wrong, Why, What to do).
* **Team View:** Level 2 organizational trend view (misalignment between departments, capability gaps).
* **Interactive Discussion:** Ability to click into a 'Failure Pattern', reveal the 'Root Causes', and view the raw 'Evidence' live in the room.
* **Workshop Notes:** Consultant can take live notes directly on the Failure Patterns that append to the final Action Plan.
* **Live Action Planning:** Assigning owners and adjusting timelines (Immediate, 30-Day, 60-Day) in real-time.

---

## 8. Implementation Tracking

The TarkaX Action Plan Engine (Layer 5.5) translates 'What should be fixed' into sequenced actions.

### MVP: Passive Tracking Board
* **Structure:** Actions are mapped to abstract roles (CEO, COO) and categorized by APQC-aligned Action Categories.
* **Horizons:** Immediate, 30-Day, 60-Day, 90-Day, 6-Month, 12-Month.
* **Operating Model:** The consultant uses this board to drive check-in meetings. It is the consultant's responsibility to update statuses (e.g., Not Started, In Progress, Blocked, Complete) based on client feedback.

### Future: Automated System
* Automated nudges, executive reminders, and integration with Jira/Asana/Monday.

### Outputs
* **Progress Reports:** Generation of implementation status PDFs for the client board.
* **Capability Growth:** Conceptual math showing how completed actions have altered the forecast (Best/Expected/Worst case).

---

## 9. Recurring Assessments

TarkaX is a continuous transformation engine, not a one-time diagnostic tool. Recurring assessments are the primary mechanism for consultants to prove value and secure renewals.

### Design
* **Quarterly Pulse Check:** Lightweight assessments focusing purely on the highest-risk areas identified in the previous Action Plan.
* **Semi-Annual Reassessment:** Medium-depth audit of the full TOHM (TarkaX Organizational Health Model).
* **Annual Reassessment:** Full baseline audit to establish the new Reality Gap and Alignment scores.

### Outputs
* **Trend Analysis:** Visualizing risk reduction and capability maturity over time.
* **Benchmark Changes:** How the client has moved relative to the L1/L2 benchmarks.

---

## 10. Revenue Model (Hypothesis)

The monetization model separates platform licensing (seat model) from usage (assessment model) to ensure low barriers to entry with massive upside for heavy usage.

| Tier | Target Audience | Pricing Structure (Hypothesis) | Value Prop |
| :--- | :--- | :--- | :--- |
| **Independent** | Solo consultants | **$99 - $299 / month**<br>+ $50 per full assessment | Access to professional diagnostic tools; win clients faster. |
| **Boutique** | 2-10 seat firms | **$499 - $1,499 / month**<br>+ $100 per full assessment | L1 Benchmarking across firm; standardized methodology. |
| **Enterprise** | Large practices | **Custom (e.g., $5,000+ / mo)**<br>+ Volume assessment pricing | Full API access, multi-tier hierarchy, advanced white-label. |
| **Government** | Govt. Advisory | **Custom** | Deep n-tier hierarchical architecture; strict data residency. |

---

## 11. Fastest Revenue Path

To generate the fastest possible consulting revenue, TarkaX must relentlessly focus on the critical path to closing a client.

### 1. Who buys first?
**Independent and Boutique Consultants.** They have the highest urgency to differentiate themselves from competitors, win RFPs, and justify higher retainers.

### 2. Why do they buy?
They need to look like McKinsey on day one. They buy TarkaX because it provides instant proprietary methodology, professional reports, and a structured mechanism to sell follow-on implementation work.

### 3. What problem are they paying to solve?
* **Problem 1:** Unpaid discovery. Consultants spend weeks doing free diagnostics to write a proposal.
* **Problem 2:** "Slide-deck delivery." Presenting a PDF that gets ignored.
* **Problem 3:** Failing to renew. Lacking a data-driven way to prove things improved.

### 4. Smallest feature set required (MVP Scope)
1. **Public Lead Magnet:** Frictionless, 5-minute single-insight preview.
2. **Consultant-Led Assessment Intake:** Simple UI to paste interview notes and URLs.
3. **Core Diagnostic Engine:** Identifying Capability Gaps and Risks.
4. **Dynamic PDF Generation:** Branded Executive Summary (MVP White Label).
5. **Workshop Mode:** The live presentation dashboard.

---

## 12. MVP vs Future Categorization

### BUILD NOW (Fastest Path to Revenue)
* Consultant-Led Assessment Mode (Mode A)
* Consultant Workspace (Active Engagements, Client Pipeline)
* Conceptual Hierarchy (Firm -> Consultant -> Client -> Assessment)
* MVP White Label (Logos, Colors, Report Branding)
* Level 1 Portfolio Benchmarking (Internal Client Comparisons)
* Workshop Mode (Live presentation UI)
* Passive Implementation Tracking Board (30/60/90 days)

### BUILD NEXT
* Collaborative Assessment Mode (Mode B - Role-based invites)
* Automated Implementation Nudges (Email reminders)
* Recurring Assessment Trend Analysis (Quarterly comparisons)
* Level 2 Global Benchmarking (TarkaX Anonymized Data)

### BUILD LATER
* Advanced White Label (Custom Domains, Portals)
* Jira / Asana / Monday integrations
* TimesFM Predictive Forecasting

### DO NOT BUILD (Out of Scope)
* CRM capabilities beyond basic lead context
* Automated survey campaigns or participation tracking engines
* System-level event logs or ERP integrations (sticking to qualitative evidence)
* LLM-driven core decision-making for Action Plans
* Document parsing / OCR for evidence collection
