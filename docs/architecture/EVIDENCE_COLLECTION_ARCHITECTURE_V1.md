# Evidence Collection Architecture V1

## 1. Executive Summary

TarkaX is evolving from a single-dimensional scoring tool (MCQ → Score → Graph) into an enterprise-grade Organizational Failure Intelligence platform. To support this, the system requires a robust **Evidence Collection Architecture**.

This document outlines the foundation for moving beyond simple assertions ("Yes, we do this") to verifiable intelligence ("Here is the artifact, the owner, and the operational narrative"). This architecture is specifically designed to support the future state of TarkaX, acting as the raw material for:
- Validation & Contradiction Engines
- Root Cause & Alignment Engines
- Failure Pattern Recognition
- Capability Benchmarking
- Automated Recommendations & Action Plans

The core philosophy of this architecture is **Intelligence over Reporting**. Every piece of data collected—or explicitly *not* collected—is structured as a signal for deterministic analysis, mapped eventually to standard APQC process groups.

## 2. Evidence Framework

The Evidence Model transitions from simple `MCQ Answer` payloads to an extensible `Answer + Evidence Records` relationship.

### Core Evidence Formats
The system supports a hybrid of structured inputs, narratives, and artifact references (stored externally in Supabase Storage). The architecture does not store binary files in the database.

**Supported Evidence Types:**
* `text_description`: Narrative explanation of a process.
* `tool_selection`: Explicit list/selection of software used.
* `process_owner`: The designated role/individual owning the outcome.
* `confidence_score`: User-reported confidence in their assertion.
* `workflow_narrative`: Step-by-step description.
* `artifact_reference`: URI pointer to uploaded screenshots, SOPs, Policies, Process Maps, PDFs, Spreadsheets.
* `external_url`: Links to live systems (e.g., Jira, Confluence).

### The "Lack of Evidence" Paradigm
A critical capability of this architecture is treating the *absence* of evidence as first-class data. A blank text field is ambiguous; an explicit "We do not track this" is a powerful diagnostic signal.

**Evidence Status Fields (`evidence_status`):**
* `PROVIDED`: Evidence is attached or documented.
* `NO_EVIDENCE_AVAILABLE`: User explicitly confirmed they lack the documentation/artifact.
* `UNKNOWN`: User does not know if the evidence exists (Knowledge Silo signal).
* `NOT_APPLICABLE`: The metric does not apply to their context.

### Confidence Index Groundwork
To support the future Validation Layer and Confidence Index, every evidence record contains metadata regarding its reliability.

**Metadata Fields:**
* `source_type`: `SELF_REPORTED` | `MANAGER_REPORTED` | `EMPLOYEE_REPORTED` | `ARTIFACT_BACKED` | `SYSTEM_GENERATED`
* `verification_status`: `UNVERIFIED` | `PARTIALLY_VERIFIED` | `VERIFIED`

*Note: APQC mapping does not occur at the point of collection to protect user experience. Evidence payloads are structured to allow downstream Extraction and Normalization layers to map data to Business Functions, Workflow Categories, and Process Groups.*

---

## 3. Audit-Type Matrix

Different organizational assessments require distinct evidence profiles to triangulate reality accurately. Below is the framework for what information is required and why.

| Audit Type | Required Information Focus | Required Evidence Profile | Why It Matters (The Intelligence Signal) |
| :--- | :--- | :--- | :--- |
| **Leadership Audit** | Strategic Intent, Resource Allocation, Governance | Strategic Rationale, Success Metrics, Defined Owners, Budget Approvals | Identifies if the organization has direction and allocated capability. Missing evidence flags **Governance Failure**. |
| **Manager Audit** | Operational Execution, Bottlenecks, Escalation | Workflow Execution Narratives, Escalation Protocols, Tool Configurations, Team KPIs | Evaluates if strategy translates to management. Missing evidence flags **Execution Gaps or Broken Feedback Loops**. |
| **Employee Audit** | Ground-Truth Reality, Friction, Adherence | Actual Steps Followed, Personal Frustrations, Shadow IT Tools Used | Validates alignment vs. reality. Missing evidence (or contradictions) flags **Knowledge Silos or Process Non-Adherence**. |
| **AI Audit** | Usage, Risk, Compliance | AI Tools Deployed (Sanctioned/Shadow), Data Policies, Security Reviews | Detects **Shadow AI** and evaluates readiness. Absence of policy evidence signals **Critical Governance Risk**. |
| **Workflow Diagnostic** | End-to-End APQC Process Health | SOP Artifacts, Process Maps, Latency Metrics, Handoff Points | Maps the structural reality of the process. Essential for deterministic bottleneck simulation. |
| **Alignment Audit** | Cross-Tier Consensus | Synthesized evidence across Leadership, Manager, and Employee tiers. | Feeds the Alignment Engine. The delta between tier responses is the core metric. |

---

## 4. Contradiction Detection Support

The **Contradiction Engine** relies on structured evidence to identify when a user's *claim* does not match their *reality*.

**Enabling Architecture:**
* **Granular Evidence Types:** Separating `Claim` (e.g., MCQ Answer = "Highly Automated") from `Evidence Type` (e.g., `tool_selection` = "Excel", `artifact_type` = "Spreadsheet").
* **Normalization Ready:** Text evidence is captured distinctly from categorical data so downstream LLMs can extract entities (e.g., "Excel") and map them to deterministic capability levels (e.g., "Level 1 - Fragile/Manual").
* **Cross-Referencing:** The `assessment_context_id` links responses across different users within the same organization, allowing the engine to compare a Manager's claim against an Employee's evidence.

**Example Detection:**
* Claim: "Strong Governance" (Level 4 Capability)
* Evidence `process_owner`: `NULL` or `UNKNOWN`
* Result: Engine flags a deterministic contradiction and downgrades the validated capability score.

---

## 5. Root Cause Support

The **Root Cause Engine** will analyze failures through a deterministic chain: `Problem → Cause → Impact → Fix`.

To make this possible, the collection architecture must capture operational context alongside the finding.

**Evidence Collected Today for Future Root Cause:**
1. **The "Why" Narrative (`workflow_narrative`):** Captures *how* the work is done, allowing AI to identify structural flaws (e.g., "We wait for email approval").
2. **The Tools Used (`tool_selection`):** Identifies technology constraints (e.g., fragmented data across 4 systems).
3. **The Escalation Path (`text_description` on specific questions):** Identifies where decisions stall.
4. **The `evidence_status`:** A status of `UNKNOWN` immediately isolates the root cause as a Knowledge/Communication Silo, rather than a technical failure.

---

## 6. Benchmarking Support

TarkaX uses capability benchmarking, which requires deep contextual metadata at the time of the assessment, independent of the static user profile.

**Assessment Context Schema:**
Captured per-assessment/audit instance:
* `industry_vertical`: e.g., "SaaS", "Manufacturing"
* `organization_type`: e.g., "Enterprise", "Government", "SMB"
* `organization_size`: e.g., "1000-5000"
* `department_function`: e.g., "RevOps", "Engineering"
* `team_size`: e.g., "50-100"
* `audit_type`: e.g., "Workflow Diagnostic"
* `geographic_region` (Optional)

This contextual block allows the Benchmark Engine to compare apples-to-apples capabilities (e.g., "Your RevOps Governance is Level 2; the baseline for 1000+ Enterprise is Level 4").

---

## 7. Alignment Support

The **Alignment Audit** compares Leadership (Intent), Managers (Execution), and Employees (Reality).

**Consistent Evidence Structures (Required Across All 3 Tiers):**
* `Claim` (The perceived maturity level).
* `Tool Selection` (What they *think* is being used).
* `Frustrations/Friction` (To measure subjective pain points at each level).
* `Process Owner` (To see if everyone agrees on who is in charge).

**Differing Evidence Structures:**
* **Leadership:** Heavy on `artifact_reference` for Strategy, Budget, and Policy.
* **Managers:** Heavy on `artifact_reference` for SOPs, Dashboards, and Escalation rules.
* **Employees:** Heavy on `workflow_narrative` and `shadow_tool` usage. Artifacts are less relevant here; lived experience is the primary evidence.

---

## 8. Failure Pattern Engine Support

The architecture supports the detection of standard Organizational Failure Patterns:

* **Shadow AI / Tool Sprawl:** Enabled by contrasting `sanctioned_tools` (Leadership) vs. `actual_tools` (Employee text/selection inputs).
* **Governance Failure:** Enabled by tracking `NO_EVIDENCE_AVAILABLE` on Policy/SOP artifacts and `UNKNOWN` on process owner fields.
* **Approval Bottlenecks:** Enabled by capturing `workflow_narrative` and specific `escalation_path` text fields.
* **Knowledge Silos:** Triggered heavily when Employees select `UNKNOWN` for processes that Managers claim are "Standardized."
* **Leadership-Employee Misalignment:** Evaluated by the delta in capability claims and `frustration_index` across tiers.

---

## 9. Database Design

### Storage Model
The architecture uses a normalized PostgreSQL relational model to support multiple distinct pieces of evidence per answer. It avoids massive nested JSONB structures to ensure queryability, indexability, and contradiction analysis. However, it leverages JSONB for flexible, non-indexed metadata.

### Tables Impacted / New Tables

1. **`assessments`** (Updated)
   - Add foreign key to a new `assessment_contexts` table for point-in-time benchmark demographic data.

2. **`assessment_contexts`** (New)
   - Stores the demographic snapshot (Industry, Org Size, Dept, etc.) used for benchmarking.

3. **`question_responses`** (Updated)
   - Maintained as the primary link between Assessment, User, and Question.

4. **`evidence_records`** (New)
   - A one-to-many relationship with `question_responses`.

### Recommended Schema Example (SQLAlchemy Model Concept)

```python
class AssessmentContext(Base):
    __tablename__ = 'assessment_contexts'

    id = Column(UUID, primary_key=True)
    assessment_id = Column(UUID, ForeignKey('assessments.id'))
    industry = Column(String)
    organization_size = Column(String)
    department = Column(String)
    # ... other benchmark dimensions

class QuestionResponse(Base):
    __tablename__ = 'question_responses'

    id = Column(UUID, primary_key=True)
    assessment_id = Column(UUID, ForeignKey('assessments.id'))
    question_id = Column(UUID, ForeignKey('questions.id'))
    selected_option_id = Column(UUID) # The MCQ Claim

    # Relationship to evidence
    evidence = relationship('EvidenceRecord', back_populates='response')

class EvidenceRecord(Base):
    __tablename__ = 'evidence_records'

    id = Column(UUID, primary_key=True)
    response_id = Column(UUID, ForeignKey('question_responses.id'))

    # The Core Signal
    evidence_status = Column(String) # 'PROVIDED', 'NO_EVIDENCE_AVAILABLE', 'UNKNOWN', 'NOT_APPLICABLE'
    evidence_type = Column(String)   # 'TEXT', 'TOOL', 'OWNER', 'ARTIFACT', 'URL'

    # The Payload
    content = Column(Text, nullable=True) # Text narrative, or tool name, or owner name
    artifact_uri = Column(String, nullable=True) # Pointer to Supabase Storage

    # Confidence & Validation Groundwork
    source_type = Column(String, default='SELF_REPORTED')
    verification_status = Column(String, default='UNVERIFIED')

    # Flexible schema for future engine needs
    metadata_payload = Column(JSONB, nullable=True)
```

### Migration Strategy
1. **Phase 1:** Create `evidence_records` and `assessment_contexts` tables. Keep existing MCQ responses intact.
2. **Phase 2:** Update the API layer to accept evidence payloads alongside MCQ answers, inserting them into `evidence_records`.
3. **Phase 3:** Introduce the `evidence_status` UI elements ("I don't have this").
4. **Phase 4:** Deprecate legacy text fields currently living inside the MCQ answer payloads (if any).

---

## 10. Frontend Design (UX)

The UI must balance the need for deep organizational intelligence with the risk of survey fatigue.

### Principles & UX Mechanics
1. **Progressive Disclosure:**
   - Users answer the MCQ first (The Claim).
   - Only highly critical questions (determined by configuration) automatically expand an Evidence Request block.
   - For other questions, evidence is an optional "Attach Evidence" button.

2. **The "Missing Evidence" Frictionless Path:**
   - Instead of forcing users to type "I don't know," provide explicit, single-click toggle states:
     - `[ Provide Details ]`
     - `[ We don't track this ]`
     - `[ I'm not sure ]`
   - Clicking the latter two instantly satisfies the evidence requirement and moves the user forward, logging the critical `evidence_status` signal without causing fatigue.

3. **Strategic Evidence Collection:**
   - **Do not** ask for evidence on every question.
   - **Do** require evidence on APQC Level 3+ capability claims (e.g., If they claim "Fully Automated", the UI dynamically mandates tool selection or process mapping).
   - **Do** require evidence for major Governance assertions (e.g., Budget, Policy Ownership).

4. **Location:**
   - Evidence collection occurs inline directly below the MCQ response, utilizing visual nesting to indicate it is supporting documentation for their claim.

---

## 11. Recommended Implementation Plan

**Step 1: Database Foundation**
- Implement Alembic migrations for `assessment_contexts` and `evidence_records`.
- Update SQLAlchemy models in `backend/models/`.

**Step 2: API Updates**
- Update POST/PUT endpoints for assessment submissions to accept an optional list of `evidence` objects matching the new schema.
- Implement business logic to handle the `evidence_status` enum.

**Step 3: Frontend State Management**
- Update the frontend assessment store to manage evidence state separately from the base MCQ answer.
- Implement the baseline Evidence UI block (Text input + Status Toggles).

**Step 4: Artifact Support (Future)**
- Integrate Supabase Storage SDK.
- Add file upload UI component.
- Map returned URIs to `artifact_uri` in the `EvidenceRecord`.

**Step 5: Intelligence Layer Readiness**
- Ensure data export/extraction scripts pull the `assessment_contexts` and normalized `evidence_records` to begin offline training/testing of the APQC mapping and Contradiction models.
