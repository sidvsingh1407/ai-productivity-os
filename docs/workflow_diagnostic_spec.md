# Workflow Diagnostic: Product & Technical Specification

## Phase 1: Define the Product

**What is Workflow Diagnostic?**
Workflow Diagnostic is a deterministic operational intelligence tool. It functions as an "Operational MRI," allowing users to submit structured details about an existing workflow to receive a comprehensive analysis of its health, bottlenecks, and risks.

**What specific problem does it solve?**
Organizations often operate with inefficient, poorly documented, or risky workflows without realizing where the specific breakdowns occur. Traditional process mapping tools (like Visio) or project management tools (like Jira, Asana) describe *what* happens or *track* the execution, but they do not automatically evaluate the *quality* or *risk* of the workflow design itself. Workflow Diagnostic solves this by programmatically identifying points of failure, excessive friction, and missing governance before execution fails.

**Who uses it?**
- Operations Managers / COOs
- RevOps / SalesOps / MarketingOps Leaders
- Systems Architects & Process Engineers
- Compliance & Governance Officers

**Why would they return to it repeatedly?**
- **Continuous Improvement:** Workflows degrade over time (team changes, new tools, scaling). Users return to run diagnostics on updated workflows to verify improvements.
- **Before Implementing New Tools:** To assess if a workflow is solid enough to be automated (automating a bad process just makes it fail faster).
- **Incident Post-Mortems:** When a critical process fails (e.g., a missed enterprise renewal), they map the workflow and diagnose it to find the structural root cause.

**What is the core value proposition?**
"Don't automate a broken process. Diagnose it first." Workflow Diagnostic provides deterministic, instant visibility into the structural integrity of business operations, removing guesswork from process optimization.

---

## Phase 2: Define the Diagnostic Engine

The V1 Diagnostic Engine is entirely **deterministic and rule-based**. It analyzes structured inputs and applies strict criteria to generate scores.

### Required Inputs (The "MRI Scan")

To ensure deterministic analysis without relying on LLM interpretation of free-text, the input must be structured.

**Core Workflow Metadata:**
- `workflow_name` (String): e.g., "Enterprise Customer Onboarding"
- `workflow_goal` (String): e.g., "Successfully transition a closed-won deal to active usage within 14 days"
- `department` (String): e.g., "Customer Success"

**Workflow Steps (Array of Objects):**
For each step in the workflow, the user defines:
1. `step_name` (String): Name of the step (e.g., "Send Welcome Email")
2. `owner` (String/Role): Who is responsible (e.g., "CSM", "Automated System", "Client") - *Crucial for Ambiguity/Governance*
3. `tools_used` (Array of Strings): Systems involved (e.g., ["Salesforce", "Marketo"])
4. `is_approval_gate` (Boolean): Does this step require someone to approve before moving on? - *Crucial for Bottlenecks*
5. `dependencies` (Array of Integers/Step IDs): Which steps must complete before this one starts? - *Crucial for Risk*
6. `estimated_time_hours` (Float): Expected duration - *Crucial for Bottleneck/Health*
7. `requires_human_handoff` (Boolean): Does the output of this step pass from one human to another? - *Crucial for Bottleneck/Ambiguity*
8. `has_audit_trail` (Boolean): Is the outcome of this step logged in an uneditable system of record? - *Crucial for Governance*

**Minimum Information Required to Generate Value:**
At least 3 steps, with defined owners, handoff flags, and approval flags. If fewer than 3 steps are provided, the system should prompt for more granularity.

---

## Phase 3: Define Analysis Output

The engine applies rules to the structured inputs to generate specific scores (0-100, where 100 is optimal/healthy).

### 1. Workflow Health Score (Overall)
A weighted average of the four primary diagnostic scores. Represents the overall operational readiness of the workflow.

### 2. Bottleneck Score
*Measures friction and delays.*
- **Rules:**
  - High percentage of steps marked `is_approval_gate` -> Lower Score (Penalty). Example: > 20% approvals is a red flag.
  - Successive steps owned by the same human owner but requiring manual handoffs -> Lower Score.
  - Single owner assigned to a disproportionate amount of estimated time -> Lower Score.

### 3. Ambiguity Score
*Measures lack of clear ownership or undefined transitions.*
- **Rules:**
  - Missing `owner` on any step -> Heavy Penalty.
  - Steps with "Team" or "Group" as owner instead of a specific role -> Penalty.
  - High ratio of human handoffs without a corresponding system tool to manage the handoff -> Penalty.

### 4. Governance Score
*Measures auditability and compliance.*
- **Rules:**
  - Steps marked `is_approval_gate` but missing `has_audit_trail` -> Heavy Penalty (approvals must be recorded).
  - Lack of a final "Verification" or "Close-out" step in workflows with high financial/time stakes -> Penalty.
  - Critical system updates without an assigned owner -> Penalty.

### 5. Execution Risk Score
*Measures structural fragility and single points of failure.*
- **Rules:**
  - High number of interdependent steps (deep chains) -> Lower Score (more things can break).
  - Single role owning more than 70% of the critical path -> Penalty (Bus factor).
  - Cross-departmental handoffs without dual-tool integration -> Penalty.

### Output Artifacts Generated:
- **Strengths:** E.g., "Clear ownership across all execution steps."
- **Weaknesses:** E.g., "Excessive manual approval gates create a 48-hour artificial delay."
- **Recommendations:** E.g., "Consolidate Step 3 and 4 approvals into a single automated governance check."
- **Priority Actions:** The top 3 changes that will raise the Health Score the most.

---

## Phase 4: Design User Journey

**Map:**
1. **Dashboard:** User sees "Diagnostics" in the main navigation alongside "Audits".
2. **Run Diagnostic (Empty State/Intro):** A brief modal or page explaining the purpose ("Map your process to find hidden bottlenecks and risks").
3. **Input Workflow (The MVP Form):** User fills out the structured form. Dynamic fields allow adding/removing steps.
4. **Analysis Loading:** A brief cinematic loading state (TARKAX style: dark, precise, scanning animation) while the deterministic engine calculates scores.
5. **Results Page (The MRI Report):** Display of the 5 core scores, visual breakdown of the workflow, and prioritized recommendations.
6. **Saved History:** The report is saved to the organization's history for future review or comparison.

**Key Considerations:**
- **Time to Value:** Must be under 5 minutes. The form must be extremely fast to fill out using keyboard navigation and sensible defaults.
- **Friction Points:** Inputting 20 steps manually is tedious. (Future phase: CSV upload or LLM generation from text. For V1: Keep the UI fast and require only a few crucial data points).
- **Confusion Risks:** Users might confuse this with an automation builder (e.g., trying to "run" it). The UI must explicitly use language like "Analyze", "Diagnose", "Submit for Review".

---

## Phase 5: Design MVP Form

The form must be the smallest real form necessary to feed the diagnostic engine.

**Workflow Context Section:**
- `Workflow Name` (Text input) -> *Identifies the report.*
- `Primary Goal` (Text input) -> *Context for future LLM recommendations; sets user intent.*

**Workflow Steps Builder (Dynamic List):**
For each step (Minimum 3 required):
- `Step Name` (Text) -> *Why: Identifies the action.*
- `Owner Role` (Text/Dropdown) -> *Why: Required for Ambiguity and Risk scoring (bus factor).*
- `Requires Approval?` (Checkbox/Toggle) -> *Why: Directly feeds the Bottleneck score.*
- `System/Tool` (Text) -> *Why: Required for Risk and Governance scoring (are things happening offline?).*
- `Manual Handoff?` (Checkbox/Toggle) -> *Why: Feeds Ambiguity and Bottleneck scores.*

*Note: In V1, we drop `estimated_time` and `dependencies` from the required inputs to drastically reduce form friction, while still gathering enough data to calculate meaningful Governance, Ambiguity, and Bottleneck scores based on approvals, tools, and handoffs.*

---

## Phase 6: Backend Requirements

### Database Models (`backend/models/diagnostic.py` - Proposed)
```python
class DiagnosticStatus(str, enum.Enum):
    pending = "pending"
    analyzing = "analyzing"
    complete = "complete"
    failed = "failed"

class WorkflowDiagnostic(Base):
    __tablename__ = "workflow_diagnostics"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    org_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("organizations.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    workflow_name: Mapped[str] = mapped_column(String, nullable=False)
    workflow_goal: Mapped[str] = mapped_column(String, nullable=False)

    # Stores the raw array of step objects
    steps_input: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # Stores the engine's deterministic output
    scores: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    findings: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    status: Mapped[DiagnosticStatus] = mapped_column(Enum(DiagnosticStatus), default=DiagnosticStatus.pending)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
```

### Pydantic Schemas (`backend/schemas/diagnostic.py` - Proposed)
```python
class DiagnosticStepInput(BaseModel):
    step_name: str
    owner_role: str
    requires_approval: bool = False
    system_tool: str | None = None
    manual_handoff: bool = False

class WorkflowDiagnosticCreate(BaseModel):
    workflow_name: str
    workflow_goal: str
    steps: list[DiagnosticStepInput]

class WorkflowDiagnosticResponse(BaseModel):
    id: uuid.UUID
    workflow_name: str
    scores: dict # { health: int, bottleneck: int, ambiguity: int, governance: int, risk: int }
    findings: dict # { strengths: list, weaknesses: list, priority_actions: list }
    status: str
    created_at: datetime
```

### API Endpoints (`backend/diagnostics/router.py` - Proposed)
- `POST /api/diagnostics/` -> Accepts `WorkflowDiagnosticCreate`, runs the deterministic scoring engine synchronously (or triggers async task), returns created record.
- `GET /api/diagnostics/{id}` -> Returns the full `WorkflowDiagnosticResponse`.
- `GET /api/diagnostics/` -> Lists all past diagnostics for the organization.
- `DELETE /api/diagnostics/{id}` -> Removes a diagnostic.

### Required Services
- `DiagnosticEngineService`: A pure Python class containing the deterministic rules. It takes the `steps` array, applies the logic defined in Phase 3, and returns a calculated dictionary of scores and generated finding strings.

---

## Phase 7: Results Page

The Results Page must feel like a high-value, executive-grade "AI Audit" report.

**Visual Layout:**
- **Header:** Workflow Name, Date, and the massive **Overall Health Score** (color-coded: Emerald for >80, Gold for 50-80, Red for <50).
- **The Scorecard Grid:** 4 distinct metric cards displaying Bottleneck, Ambiguity, Governance, and Risk scores, with a one-sentence interpretation (e.g., "Governance: 40/100 - High risk of unrecorded approvals").
- **The Structural Findings:**
  - **Critical Weaknesses:** Highlighting specific steps (e.g., "Step 3 (Legal Approval) creates an unmonitored manual handoff").
  - **Priority Actions:** 3 concrete recommendations (e.g., "Require a system of record for the Legal Approval step").
- **Workflow Map Visualization:** A read-only, vertical timeline or node-graph visual representation of the steps the user inputted, highlighting the "red" steps that caused low scores.

---

## Phase 8: Retention Loop

**Why run it repeatedly?**
- To track the ROI of operational changes. If a user implements a recommendation (e.g., automating a handoff), they return to run the diagnostic again to see their Bottleneck Score improve.
- Periodic governance reviews (quarterly process audits).

**Design:**
- **Diagnostic History Table:** A dashboard view showing all past runs, sortable by Health Score.
- **Trend Indicators:** If a workflow with the exact same name is run multiple times, the UI should show "Health Score: 85 (+12 from last run)".

---

## Phase 9: Implementation Roadmap

### Phase 1: Core Engine & Data Foundation (P0)
- **Backend:** Create DB models (`models/diagnostic.py`), Pydantic schemas, and SQLAlchemy migrations.
- **Backend:** Implement the `DiagnosticEngineService` (deterministic rule logic).
- **Backend:** Implement CRUD API endpoints (`/api/diagnostics/`).
- **Effort:** 1-2 Days.

### Phase 2: MVP Frontend Input & Output (P0)
- **Frontend:** Build the structured form UI (`WorkflowDiagnosticForm.tsx`) with dynamic step addition using `react-hook-form` and `zod`.
- **Frontend:** Build the Results Report page (`DiagnosticReport.tsx`) using Recharts for any score visualizations and Shadcn cards for findings.
- **Frontend:** Integrate with `apiClient`.
- **Effort:** 2-3 Days.

### Phase 3: Dashboard & History (P1)
- **Frontend:** Add the Diagnostics index view to the dashboard.
- **Frontend:** Implement the "Trend Indicator" logic for repeated runs.
- **Effort:** 1 Day.

### Phase 4: Integration with AI Audit (P2 - Future)
- **Backend/Frontend:** Add ability to launch a Workflow Diagnostic pre-filled with context derived from a specific AI Audit finding.
- **Effort:** TBD.

---

## Phase 10: Risks & Assumptions

**Risks:**
- **Form Fatigue:** Users may find entering structured step data tedious. *Mitigation: Keep the required fields per step to an absolute minimum (5 simple fields).*
- **Overly Punitive Scoring:** If the deterministic engine is too harsh, users may feel discouraged. *Mitigation: Tune the scoring logic to ensure a baseline score of ~50 for average workflows, saving red scores (<40) for truly broken processes.*
- **Perception as a Builder:** Users might expect to "execute" the workflow after designing it. *Mitigation: Extremely clear copywriting. "This is a diagnostic tool, not an execution engine."*

**Assumptions:**
- Users possess enough internal knowledge of their own workflows to accurately map the steps and owners.
- The TARKAX user values objective scoring over qualitative "advice."
- The deterministic rules defined in V1 provide sufficient value without requiring an LLM to parse the workflow logic.