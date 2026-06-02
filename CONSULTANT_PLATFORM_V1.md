# TarkaX Consultant & Government Platform (Program 6)
## Organizational Failure Intelligence & Transformation OS

## Executive Summary
TarkaX is evolving from a standalone assessment tool into a comprehensive **Transformation Operating System**. Program 6 introduces the Consultant and Government Platform, designed specifically for consulting firms (Deloitte, PwC, boutique firms) and large government entities.

The core operating principle is that TarkaX must support the entire consulting lifecycle: **Assessment → Diagnosis → Workshop → Implementation → Tracking → Reassessment**, enabling deep, cross-client analytics and hierarchical risk rollups.

---

## 1. Consulting Firm Operating Model
### 1.1 The Consultant Journey
TarkaX replaces fragmented spreadsheets and slide decks with a unified, end-to-end transformation workflow.

1. **Lead / Context Phase:**
   - Not a CRM. Captures essential context: Client Name, Industry, Organization Type, Size, Assessment Goal, Primary Contact, and Consultant Notes.
2. **Assessment Phase (Dual Mode):**
   - **Mode A (Consultant-Led):** Consultant interviews the client and runs the assessment directly via the platform.
   - **Mode B (Collaborative):** TarkaX generates distinct assessment links for different client stakeholders (e.g., CEO, Manager, Employee) to capture multi-perspective realities (powering the Alignment & Contradiction engines).
3. **Diagnosis Phase:** Intelligence engines (Root Cause, Failure Risks, Capability Gaps) process the evidence.
4. **Workshop Phase:** Consultant presents findings interactively using the Workshop Dashboard.
5. **Implementation Phase:** Action plans are generated, prioritized, and assigned owners.
6. **Reassessment Phase:** Continuous tracking of KPIs and delta-improvements over time.

### 1.2 Multi-Client Portfolio Management (Data Isolation)
To support large firms, TarkaX utilizes a strict hierarchical data isolation model:

```text
Firm (e.g., Deloitte)
 └── Partner (e.g., Partner A - Financial Services)
      └── Consultant (e.g., Consultant X)
           ├── Client 1 (Bank Alpha)
           └── Client 2 (Insurance Beta)
```

- **Firm Admins** can view all aggregated data across the firm.
- **Partners** can only view analytics and clients within their designated portfolio.
- **Consultants** can only access explicitly assigned clients.
- **Client Benchmarking:**
  - *Level 1 (Internal Portfolio):* Compare Client 1 vs Client 2.
  - *Level 2 (Global Benchmark):* Compare against the anonymized TarkaX ecosystem index.

### 1.3 White Label Capabilities (V1)
In V1, white-labeling is constrained to visual branding to maintain TarkaX domain integrity while allowing firms to present polished deliverables.
- **Firm Logo Injection:** Displayed on dashboards and reports.
- **Color Theming:** Primary/Secondary color application to the UI and charts.
- **Report Branding:** PDF exports include the consulting firm's branding and formatting.
*(Note: Custom domains and proprietary taxonomy injection are reserved for V2).*

### 1.4 Implementation Tracking
TarkaX tracks execution to ensure transformation succeeds. V1 includes a lightweight, built-in tracking engine:
- **Workflow:** Recommendation → Action Plan → Owner → Due Date → Status → Progress.
- **Reassessment:** Track the delta between initial capability gaps and current state post-implementation.
*(Note: Future phases will integrate with Jira, Asana, Monday, and ClickUp).*

---

## 2. Government Architecture
### 2.1 The Government Assessment Model
Government entities require deeper, n-tier hierarchies compared to standard corporate clients. The architecture supports complex, multi-level rollups to monitor policy implementation, compliance, and department performance.

**Hierarchical Structure:**
```text
Ministry (e.g., Ministry of Health)
 └── Department (e.g., Dept of Public Health)
      └── Agency (e.g., CDC)
           └── Program (e.g., Vaccination Outreach)
                └── Initiative (e.g., Rural Distribution)
```

### 2.2 Risk and Intelligence Rollups
Risks, Capability Gaps, and Contradictions are aggregated bottom-up.
- An **Initiative Risk** (e.g., budget deficit, lack of IT infrastructure) bubbles up to impact the **Program Risk**.
- **Program Risks** aggregate to determine the overall **Department Risk** profile.
- This allows Ministry-level executives to pinpoint exact points of failure within a massive bureaucracy.
- **Capabilities:** Department Comparison, Policy Implementation Tracking, Compliance Monitoring, and Program Benchmarking.

---

## 3. Data & Permission Models

### 3.1 User Roles
1. **Firm Admin:** Unrestricted access to the entire consulting firm's portfolio. Manages billing, white-labeling, and global user provisioning.
2. **Partner (Portfolio Manager):** Read/Write access restricted to their assigned portfolio of clients/consultants.
3. **Consultant (Operator):** Read/Write access limited strictly to explicitly assigned clients. Runs workshops, triggers assessments, and manages action plans.
4. **Client Admin:** Client-side stakeholder who can view dashboards, track implementation progress, and assign action owners within their organization.
5. **Client Respondent:** A user who only has access to complete a specific assessment (e.g., Employee Audit). No dashboard access.

### 3.2 Permission Matrix
| Feature | Firm Admin | Partner | Consultant | Client Admin | Client Respondent |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Global Portfolio View | Yes | No | No | No | No |
| Portfolio Level View | Yes | Yes (Assigned) | No | No | No |
| Cross-Client Analytics | Yes | Yes (Assigned) | No | No | No |
| Client Dashboard | Yes | Yes (Assigned) | Yes (Assigned) | Yes | No |
| Manage Action Plans | Yes | Yes | Yes | Yes | No |
| Run Assessments | Yes | Yes | Yes | No | No |
| Complete Assessment | No | No | No | Yes | Yes |

### 3.3 Core Data Models
* **`Tenant` (Firm/Ministry):** The top-level billing and isolation boundary.
* **`Portfolio` (Partner/Department):** Logical grouping of clients/agencies.
* **`Client` (Organization/Agency):** The entity being assessed.
* **`Assessment_Context`:** The initial "Lead" data (Industry, Size, Goal).
* **`Assessment_Instance`:** A specific run of an assessment (e.g., Q1 2024 Audit).
* **`Action_Item`:** Tied to a specific Recommendation, tracking Owner, Status, Due Date, and Progress.

---

## 4. Workshop Mode
To facilitate high-value consulting engagements, TarkaX features an **Interactive Workshop Mode** designed for live presentation, replacing static slide decks.

### 4.1 Workshop Dashboard Components
The Workshop Dashboard is optimized for screen sharing and live navigation:
- **Executive Summary:** High-level narrative of organizational health.
- **Interactive Findings:** Drill-down capability from Symptoms → Root Causes → Evidence.
- **Benchmark Gaps:** Visual comparison against internal portfolio or global TarkaX indexes.
- **Failure Risks:** Prioritized heatmaps of critical vulnerabilities.
- **Recommendations & Action Priorities:** Live mapping of what needs to be fixed and in what sequence (Immediate, 30-Day, 60-Day, 90-Day).
- **Discussion Prompts:** Auto-generated questions tailored to the specific Root Causes, intended to stimulate client debate during the workshop.

*(Note: While PDF export is available, the primary use case is interactive, live navigation).*

---

## 5. Monetization Strategy
The monetization model is built around Platform Licensing + Usage (Assessments). It avoids penalizing firms for adding clients (which drives data network effects for the TarkaX index) while monetizing the depth of usage.

### Tier 1: Independent Consultant
- **Target:** Solo practitioners.
- **Model:** Flat monthly/annual platform fee + limited assessment credits per month.
- **Features:** 1 Seat, Basic Benchmarking, Standard Export.

### Tier 2: Boutique Consulting Firm
- **Target:** Firms with 2-50 consultants.
- **Model:** Base platform fee (includes 5 seats) + per-seat expansion + metered assessments.
- **Features:** Portfolio Management (1 Level), White-labeling (V1), Workshop Mode, Implementation Tracking.

### Tier 3: Enterprise Consulting Firm
- **Target:** Big 4, MBB, Large SIs (Accenture, Deloitte).
- **Model:** Custom Annual Enterprise License (Platform Fee + Volume Assessments).
- **Features:** Multi-level Portfolio Isolation, Advanced API Access, SSO, Custom Framework Injection (Future V2), Custom Data Residency.

### Tier 4: Government Organization
- **Target:** Ministries, Federal Agencies.
- **Model:** Dedicated Instance / Private Cloud Licensing. Annual contract based on hierarchical complexity and department volume.
- **Features:** N-Tier Hierarchical Rollups, Strict Compliance/Security controls, Custom Policy Implementation Tracking.

---

## 6. Future Features Roadmap

### P0 (Critical Path - V1 Launch)
- Dual Operating Modes (Consultant-Led vs. Collaborative).
- Multi-Client Portfolio Management (Data Isolation logic: Firm → Partner → Consultant → Client).
- Government N-Tier Hierarchy and Risk Rollups.
- Interactive Workshop Mode.
- Implementation Tracking Engine (Native TarkaX tracking).
- Roles & Permissions Engine (Firm Admin, Partner, Consultant, Client Admin, Respondent).

### P1 (Fast Follows)
- White Labeling V1 (Logo, Colors, PDF Branding).
- Level 1 & Level 2 Benchmarking (Internal vs. Global).
- Payment processing for the Monetization Tiers (Stripe integration for Boutique/Independent).

### P2 (Strategic Expansion)
- Custom Domain White Labeling (V2).
- Proprietary Framework Injection (Allowing firms to map TarkaX to their own APQC/custom models).
- Third-party Implementation Integrations (Jira, Asana, Monday, ClickUp).
- TarkaX Global Benchmark Index API.
