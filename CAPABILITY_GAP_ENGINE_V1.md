# Capability Gap Engine (v1)

## 1. Executive Summary

The Capability Gap Engine represents a critical shift in TarkaX's Organizational Failure Intelligence Platform. Moving beyond traditional "deficiency scoring" (e.g., "Governance Score = 61"), this engine is designed to answer a singular, strategic question: **"Given the organization's demographic profile, operational realities, and intelligence signals, what capabilities should reasonably exist, but currently do not?"**

By shifting the diagnostic focus from quantitative abstraction to structural reality, the Capability Gap Engine acts as the bridge between theoretical capability models and pragmatic organizational design. Positioned in Layer 4 (Intelligence) of the TarkaX architecture, the engine synthesizes outputs from the Validation, Root Cause, Failure Pattern, and Alignment engines to generate prescriptive, actionable capability gaps.

**Core Philosophy:**
*   **Absence over Deficiency:** We identify missing organizational artifacts, roles, and processes, not just low scores.
*   **Contextual Expectation:** Expected capabilities are generated dynamically via a multi-dimensional matrix (Industry + Size + Type + Department), ensuring organizations are measured against realistic operational standards rather than generic utopias.
*   **Deterministic Intelligence:** Determinations are rules-based and logically auditable, derived from empirical organizational evidence.

---

## 2. Capability Taxonomy

The Capability Gap Engine operates on a 3-layer hierarchical taxonomy that fuses cross-functional organizational realities with the standardized rigor of APQC workflow definitions. The engine primarily operates at Layer C, inheriting structural context from Layers A and B.

### Layer A: Cross-Organizational Capability Domains
Broad organizational domains that transcend specific workflows or departments.
*   **Governance**
*   **Operations**
*   **AI Adoption**
*   **Knowledge Management**
*   **Risk Management**
*   **Workforce Capability**
*   **Reporting & Analytics**
*   **Change Management**

### Layer B: APQC Workflow Domains
Standardized functional domains derived from APQC taxonomies.
*   **Finance**
*   **Human Resources (HR)**
*   **Procurement**
*   **Marketing**
*   **Sales**
*   **Information Technology (IT)**
*   **Customer Service**
*   **Government Services**

### Layer C: Specific Capabilities (The Detection Layer)
The tangible processes, artifacts, roles, or mechanisms that an organization either possesses or lacks.

**Examples:**
*   **Finance (Layer B) / Governance (Layer A)**
    *   $\rightarrow$ Invoice Processing Ownership
    *   $\rightarrow$ Approval Routing Protocol
    *   $\rightarrow$ Financial SLA Tracking Mechanism
*   **HR (Layer B) / Workforce Capability (Layer A)**
    *   $\rightarrow$ Recruitment Workflow Documentation
    *   $\rightarrow$ Onboarding Governance Board
    *   $\rightarrow$ Standardized Performance Review Process
*   **AI Adoption (Layer A)**
    *   $\rightarrow$ Formal AI Usage Policy
    *   $\rightarrow$ AI Literacy Training Program
    *   $\rightarrow$ AI Governance Committee

---

## 3. Capability Maturity Mapping

The engine measures an organization's structural capability against the TarkaX 5-Level Maturity Model. These levels represent operational reality and resilience, specifically avoiding aspirational (e.g., "Transformational") branding in favor of measurable stability.

| Level | Designation | Description | Evidence Expectation |
| :--- | :--- | :--- | :--- |
| **L1** | **Fragile** | Highly dependent on heroics. Capabilities are undocumented, unstructured, and highly vulnerable to failure or staff turnover. | Ad-hoc or missing. |
| **L2** | **Emerging** | Capabilities exist in pockets. Basic awareness is present, but execution is inconsistent and unstandardized across the enterprise. | Partial documentation, tribal knowledge. |
| **L3** | **Operational** | Capabilities are formally defined, documented, and actively managed. Processes are repeatable and predictably executed. | Standard Operating Procedures (SOPs), designated owners. |
| **L4** | **Scaled** | Capabilities are deeply integrated across workflows. Automation, continuous measurement, and proactive risk management are present. | System integration, active SLAs, cross-departmental alignment. |
| **L5** | **Resilient** | Capabilities adapt to external shocks seamlessly. Predictive intelligence and self-healing workflow mechanics are fully embedded. | Predictive metrics, automated governance enforcement. |

### Capability Expectation Example: AI Adoption Domain
*   **Target State:** *Operational (L3)*
*   **Expected Capabilities:**
    *   $\checkmark$ Formal AI Usage Guidelines
    *   $\checkmark$ Standardized AI Training Program
    *   $\checkmark$ AI Workflow Automation Integration
*   **Missing Capabilities:**
    *   $\times$ AI Governance Committee
*   **Conclusion:** Capability Gap Detected.

---

## 4. Integration Architecture

The Capability Gap Engine resides in **Layer 4 (Intelligence Layer)** of the TarkaX platform. It operates late in the intelligence pipeline, ensuring that its logic is informed by validated evidence, root causes, and behavioral realities (contradictions/alignment gaps).

### Engine Sequencing
1.  **Layer 1: Assessment Framework** (Raw inputs & stated reality)
2.  **Layer 2: Validation Layer & Contradiction Engine** (Evidence verification & reality gaps)
3.  **Layer 3: Diagnosis (Root Cause Engine)** (Why are things failing?)
4.  **Layer 4: Intelligence**
    *   *Failure Pattern Engine* (Macro-level systemic issues)
    *   *Benchmark Engine* (Expected baselines)
    *   *Alignment Engine* (Perceptual deltas across hierarchy)
    *   $\rightarrow$ **Capability Gap Engine** (Synthesizes the above to output explicit structural missing capabilities)

**Data Flow Context:**
The Capability Gap Engine does not simply parse raw assessment answers. Instead, it queries the downstream intelligence artifacts: "Based on the identified Root Cause of X, and the Benchmark expectation of Y, what specific Layer C Capability is structurally absent?"

---

## 5. Capability Detection Logic

The engine uses a **Multi-Dimensional Matrix** to dynamically assemble the expected capability profile of an organization. TarkaX does not use mutually exclusive buckets; it fuses dimensions to generate a highly precise organizational profile.

**The Base Formula:**
`Expected Capabilities = F(Industry) + F(Org Type) + F(Org Size) + F(Department) + F(Target Maturity)`

**Example Demographic Slicing:**
*   **Organization Type:** Consulting Firm
*   **Size:** Enterprise (5000+ employees)
*   **Industry:** Technology
*   **Department:** Operations
*   **Target Maturity Baseline:** Scaled (L4)

**Logic Resolution:**
The engine pulls all required capabilities for *Enterprise*, unions them with requirements for *Consulting Firms*, and filters them through *Technology/Operations*. It then compares this dynamic "Expected Profile" against the validated evidence collected during the assessment. If a required capability is missing or unevidenced, a gap is flagged.

---

## 6. Gap Risk Classification Framework

When a gap is identified, it is not merely listed—it is contextualized in terms of operational impact and business risk.

**Risk Dimensions:**
*   **Capability Gap:** (Expected State - Current State)
*   **Business Criticality:** How essential is this capability to the organization's core value stream?
*   **Failure Exposure:** What is the organizational blast radius if this capability remains absent?

**Priority Classification:**
*   **Low:** Missing capability causes minor inefficiencies; limited localized impact.
*   **Moderate:** Workflow drag, moderate process debt, or delayed execution.
*   **High:** Significant risk of workflow failure, regulatory exposure, or severe operational bottleneck.
*   **Critical:** Systemic organizational vulnerability. Immediate intervention required to prevent critical failure.

---

## 7. Example Outputs

Outputs from the Capability Gap Engine explicitly avoid numeric abstraction, focusing entirely on structural narrative and actionable organizational design.

### Example 1: Missing Governance Mechanism
*   **Missing Capability:** Formal AI Governance Policy
*   **Layer A/B Mapping:** AI Adoption (Layer A) / IT (Layer B)
*   **Risk:** Uncontrolled AI Usage ("Shadow AI")
*   **Impact:** Data leakage, compliance exposure, and inconsistent tooling.
*   **Priority:** High
*   **Recommended Action:** Establish and distribute an enterprise-wide AI Governance Framework dictating approved tools, data handling, and vendor security review processes.

### Example 2: Missing Operational Role
*   **Missing Capability:** Defined Workflow Ownership
*   **Layer A/B Mapping:** Operations (Layer A) / Procurement (Layer B)
*   **Risk:** Approval Delays & Abandoned Requests
*   **Impact:** Increased cycle time and unclear accountability for stalled procurements.
*   **Priority:** Moderate
*   **Recommended Action:** Assign named workflow owners (Process Champions) for all critical procurement pathways, complete with SLA tracking responsibilities.

---

## 8. System Implications

This section details the architectural updates required to integrate the Capability Gap Engine into the existing TarkaX ecosystem.

### Database Implications
New PostgreSQL tables will be introduced within the intelligence schema, adhering to TarkaX's normalized relational model constraints.

*   **`intelligence.capability_domains_a`**
    *   **Keys:** `id`, `name`, `description`
    *   **Purpose:** Stores Layer A cross-organizational domains (e.g., Governance).
*   **`intelligence.capability_domains_b`**
    *   **Keys:** `id`, `apqc_id_reference`, `name`
    *   **Purpose:** Stores Layer B APQC mapped domains (e.g., Procurement).
*   **`intelligence.capabilities_c`**
    *   **Keys:** `id`, `domain_a_id`, `domain_b_id`, `name`, `description`
    *   **Purpose:** The master dictionary of all identifiable organizational capabilities.
*   **`intelligence.capability_rules_matrix`**
    *   **Keys:** `id`, `capability_c_id`, `industry`, `org_type`, `org_size`, `department`, `required_maturity_level`
    *   **Purpose:** The deterministic rules engine defining *when* a capability is expected.
*   **`intelligence.assessment_capability_gaps`**
    *   **Keys:** `id`, `assessment_id`, `capability_c_id`, `risk_level`, `impact_description`, `recommended_action`
    *   **Purpose:** Stores the materialized gaps detected for a specific assessment run.

### API Implications
New RESTful endpoints must be added to the FastAPI microservices to trigger and retrieve capability gap intelligence.

*   `POST /api/v1/intelligence/capability-gaps/detect`
    *   **Payload:** `{ "assessment_id": "uuid" }`
    *   **Action:** Triggers the rules engine. Queries demographic context, retrieves expected capabilities, maps against Assessment/Evidence data, and persists the gaps.
*   `GET /api/v1/intelligence/assessments/{assessment_id}/capability-gaps`
    *   **Response:** JSON array of identified gaps including Domain A/B mappings, Risk Level, Impact, and Recommendations. Used primarily by Layer 5/6 downstream consumers.

### Implications for Report V2 (Layer 6)
The Capability Gap Engine fundamentally alters the final TarkaX assessment deliverable.
*   **Deprecation of Arbitrary Scores:** Generic "Score = X%" widgets will be replaced or severely de-emphasized.
*   **New Visualization UI:** The report will require a "Capability Heatmap" or a "Missing Capability Matrix", displaying Layer A vs Layer B grids with missing capabilities explicitly highlighted.
*   **Executive Action Plan Generation:** Outputs from the engine will directly feed the final recommendations page, translating directly into actionable consultant-style roadmaps (e.g., "Implement these 4 capabilities to reach the Scaled maturity tier in Q3").

### Identified Codebase Impact Surface
The following operational areas/services will require modification:
*   `services/intelligence/capability_engine.py` (New Rules Engine service)
*   `models/intelligence.py` (SQLAlchemy / Pydantic models for the new capabilities schema)
*   `api/routers/intelligence.py` (New endpoints)
*   `services/reporting/report_generator.py` (Updating V2 report generation to consume gap objects instead of raw scores)

### Future Enhancements
*   **Predictive Gap Modeling:** Utilizing the Phase 5 Forecasting Engine (TimesFM) to predict *when* an emerging capability gap will become a critical failure based on expected organizational growth.
*   **Dynamic APQC Generation:** Using LLM-assisted tools (strictly isolated from the deterministic scoring model) to map unstructured text directly into Layer C capability dictionaries for novel industries.