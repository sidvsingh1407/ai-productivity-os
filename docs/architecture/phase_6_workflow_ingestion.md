# Phase 6: Workflow Ingestion Engine Architecture

## Part 1: MiroFish Analysis

MiroFish is an AI prediction engine powered by multi-agent simulations that constructs a digital world from seed data (documents/stories/news) using the **Zep Cloud API** for GraphRAG and knowledge graph generation, combined with **OASIS** for multi-agent simulation.

### What MiroFish Already Does
1. **Extraction & Parsing:** It handles text extraction from `.pdf`, `.md`, and `.txt` files (`FileParser`). It has a multi-level fallback encoding mechanism (UTF-8 -> `charset_normalizer` -> `chardet` -> replace) to ensure text extraction stability. It chunks text based on size, overlaps, and natural punctuation (`TextProcessor`).
2. **Graph Construction via Zep:** It uses `GraphBuilderService` to interact with Zep Cloud to dynamically create Ontology structures (`EntityModel` and `EdgeModel` generated dynamically via `type()` in Python), feed chunks in batches as "episodes", and wait for processing using a polling mechanism on background threads.
3. **Simulation & Agents:** It extracts entities and profiles (personas, behaviors) into an OASIS environment and runs asynchronous multi-agent interactions to predict social outcomes and public opinion trajectories. It provides features like interviewing specific agents (`SimulationRunner`, `ZepTools`).
4. **Task/Project Scoping:** Operations are scoped to persistent Projects (saving configs to JSON on disk). Operations run in background threads (`TaskManager`) and emit progress callbacks that are polled by the frontend.

### Reusable Components & Techniques
- **Text & Document Chunking Strategy:** The sliding-window chunking with sentence-boundary detection in `TextProcessor/FileParser` is solid and can be reused for OCR'd text extraction.
- **Robust Encoding Detection:** The multi-tier encoding fallback in `_read_text_with_fallback` is an excellent strategy for arbitrary text files.
- **Background Task Management:** The lightweight callback/progress status approach for long-running extractions (e.g., waiting for graphs to build) without complex task queues (like Celery) is useful for early-stage TARKAX.

### Limitations
- **Opaque Extraction Logic (Vendor Lock-in):** Zep Cloud handles the actual NLP text-to-graph extraction black-box. We cannot use this for TARKAX because we need deterministic, relational persistence mapped to our specific ontology, not a cloud graph service.
- **No Native Image/Shape Parsing:** MiroFish handles text-based PDFs but lacks OCR or bounding-box connector detection required for BPMN/Miro exports (images).
- **Disk-based Persistence:** MiroFish uses local file storage for projects and SQLite/JSON dumps, lacking a scalable, normalized RDBMS architecture for complex graph querying.
- **Generic Ontology:** Its ontology logic tries to find 10 generic entity types per document dynamically. TARKAX requires a strict, pre-defined operational APQC ontology.

### Architecture Overview
MiroFish acts as a pipeline orchestrator. Document -> `FileParser` -> LLM Ontology Prompt -> Dynamic Pydantic Classes -> Zep Graph Creation -> Poll Completion -> `OASIS` Simulation. TARKAX must instead orchestrate: Document -> OCR/CV Shape Extraction -> TARKAX APQC Ontology Mapper -> Relational Graph Storage -> Deterministic Rules Engine.

---

## Part 2: TARKAX Ingestion Architecture

The TARKAX ingestion flow leverages a hybrid deterministic/AI approach, bypassing generic GraphRAG tools in favor of operational intelligence.

### Service Layer Design

* **WorkflowUploadService**
  * Handles raw file uploads via API.
  * Uploads original artifacts to **Supabase Storage** (e.g., `workflows/artifacts/`).
  * Creates an initial `workflow_graphs` database record (Status: `PROCESSING`).
* **WorkflowExtractionService**
  * **Images (PNG/JPG):** Runs OCR (e.g., Tesseract/EasyOCR) and Shape/Line Detection (OpenCV) to identify bounding boxes (nodes) and connecting lines (edges).
  * **Structured/Text (BPMN/PDF):** Uses `FileParser` techniques to extract raw structure.
  * Outputs an intermediate `RawGraph` JSON representation (unnormalized nodes and edges).
* **WorkflowOntologyMapper**
  * Invokes Multimodal LLM (GPT-4o / Claude 3.5 Sonnet) *strictly for normalization*.
  * Input: `RawGraph` + Context + Image.
  * Output: Enforces the TARKAX Node Types and Edge Types onto the raw data, maintaining 80% deterministic constraints.
* **WorkflowGraphBuilder**
  * Validates the normalized JSON against Zod/Pydantic schemas.
  * Persists the normalized structure into the relational tables (`workflow_nodes` and `workflow_edges`).
  * Updates `workflow_graphs` status to `COMPLETED`.
* **WorkflowDiagnosticRunner**
  * A deterministic rules-engine that queries the relational graph representation.
  * Iterates through configurable `DiagnosticRule`s evaluating constraints (e.g., degrees of nodes, cycle detection) to output a 0-100 Health Score.
* **WorkflowRecommendationEngine**
  * Consumes the `DiagnosticReport`.
  * Maps identified risks (e.g., bottleneck on a single node) to predefined mitigation strategies and APQC best practices.

---

## Part 3: Workflow Graph Specification

We define a strict operational ontology, discarding free-form knowledge graph concepts.

### Node Types
Represent the steps or states in a process.

* **START**: The initiation point of a workflow.
* **END**: The termination point of a workflow.
* **TASK**: A standard operational action (manual or system-based).
* **APPROVAL**: A step requiring human or system authorization.
* **DECISION**: A conditional branching point (e.g., XOR gateway).
* **WAITING**: A point where the process pauses for an external event or time threshold.
* **HANDOFF**: A transfer of responsibility between departments or roles.
* **AUTOMATION**: A task entirely executed by a system/script without human intervention.

### Edge Types
Represent the flow and constraints between nodes.

* **SEQUENTIAL**: Standard linear progression from node A to node B.
* **PARALLEL**: Simultaneous flow execution (e.g., AND gateway split).
* **DEPENDENCY**: Node B cannot begin until Node A meets a specific condition, but they are not strictly sequential in the main flow.
* **APPROVAL_FLOW**: Specifically connects a `TASK` to an `APPROVAL` node, indicating a required governance check.

---

## Part 4: APQC Mapping

Every ingested workflow must be classified against the American Productivity & Quality Center (APQC) Process Classification Framework (PCF).

### Mapping Strategy
During the **WorkflowOntologyMapper** phase, the LLM evaluates the entire workflow graph context and maps the overarching process to a standard APQC Category and Process Group.

* **Marketing**: e.g., Campaign Management, Lead Generation.
* **Sales**: e.g., Opportunity Management, Order Processing.
* **HR**: e.g., Onboarding, Payroll Processing.
* **Finance**: e.g., Accounts Payable, Expense Management.
* **Procurement**: e.g., Vendor Selection, Purchase Requisition.
* **IT**: e.g., Incident Management, Change Management.
* **Customer Service**: e.g., Ticket Resolution, Warranty Claims.
* **Governance**: e.g., Audit Compliance, Risk Assessment.

The assigned APQC classification determines which diagnostic benchmark rules apply.

---

## Part 5: Diagnostic Engine

The Diagnostic Engine applies a configurable Rules-Engine (not hardcoded `if/else` logic) to evaluate relational graph data.

### Architecture
* **DiagnosticDimension**: The category of health (e.g., Bottlenecks).
* **DiagnosticRule**: A specific SQL query or graph traversal algorithm executed against the workflow.
* **DiagnosticWeight**: Configurable penalty applied to the Health Score (0-100 base) if the rule triggers.

### Dimensions Evaluated
1. **Bottlenecks:** Rules detecting nodes with high in-degree (>3) but low out-degree, indicating queue buildup.
2. **Governance:** Rules verifying critical paths contain `APPROVAL` nodes before `END` states.
3. **Visibility:** Rules identifying "black box" sub-processes or sequences lacking status reporting.
4. **Automation:** Ratio of `TASK` vs `AUTOMATION` nodes in repetitive loops.
5. **Compliance:** Detection of unapproved `HANDOFF`s between sensitive departments.
6. **Throughput:** Path length analysis (longest path) predicting process execution time.
7. **Knowledge Dependency:** Tasks assigned to specific individuals rather than roles.
8. **Handoff Risk:** Excessive `HANDOFF` edges between different organizational domains (e.g., Sales -> IT -> Finance back-and-forth).

---

## Part 6: Recommendation Engine

Triggered post-diagnosis, mapping deterministic rule failures to actionable operational advice.

* **Bottleneck Recommendations:** "Consider splitting [Node X] into parallel streams or automating initial triage."
* **Automation Opportunities:** "Node sequence [A -> B -> C] contains 100% manual tasks. Investigate RPA integration for [B]."
* **Governance Improvements:** "High compliance risk: Add an `APPROVAL` node prior to [Financial Transfer Node]."
* **Workflow Redesign Suggestions:** "Eliminate redundant `WAITING` states detected between [Handoff 1] and [Handoff 2]."

---

## Part 7: Implementation Plan

### Database Schema (Relational PostgreSQL)

```sql
-- Core Workflow
CREATE TABLE workflow_graphs (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    apqc_category VARCHAR(100),
    apqc_process_group VARCHAR(100),
    health_score INTEGER,
    status VARCHAR(50), -- PROCESSING, COMPLETED, FAILED
    artifact_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Nodes
CREATE TABLE workflow_nodes (
    id UUID PRIMARY KEY,
    graph_id UUID REFERENCES workflow_graphs(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- START, TASK, APPROVAL, etc.
    department VARCHAR(100),
    metadata JSONB -- Flexible for coordinates, extracted raw text
);

-- Edges
CREATE TABLE workflow_edges (
    id UUID PRIMARY KEY,
    graph_id UUID REFERENCES workflow_graphs(id) ON DELETE CASCADE,
    source_node_id UUID REFERENCES workflow_nodes(id) ON DELETE CASCADE,
    target_node_id UUID REFERENCES workflow_nodes(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- SEQUENTIAL, PARALLEL, etc.
    condition_text TEXT,
    metadata JSONB
);

-- Diagnostics Rules Engine Configuration
CREATE TABLE diagnostic_rules (
    id UUID PRIMARY KEY,
    dimension VARCHAR(50), -- Bottleneck, Governance
    rule_identifier VARCHAR(100) UNIQUE,
    weight INTEGER NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    description TEXT
);

-- Diagnostic Results
CREATE TABLE workflow_diagnostics (
    id UUID PRIMARY KEY,
    graph_id UUID REFERENCES workflow_graphs(id) ON DELETE CASCADE,
    rule_id UUID REFERENCES diagnostic_rules(id),
    affected_node_ids UUID[],
    score_penalty INTEGER,
    message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### API Endpoints (FastAPI)
* `POST /api/v1/workflows/upload`: Receives file, uploads to Supabase, queues extraction, returns Graph ID.
* `GET /api/v1/workflows/{graph_id}`: Returns normalized JSON representation of nodes and edges for frontend React Flow visualization.
* `GET /api/v1/workflows/{graph_id}/diagnostics`: Runs or retrieves the Diagnostic Report.
* `POST /api/v1/workflows/{graph_id}/reprocess`: Triggers extraction pipeline again.

### Frontend Components (React/Vite)
* **WorkflowUploader**: Drag-and-drop component utilizing `shadcn/ui`.
* **WorkflowCanvas**: Recharts/React Flow integration to render the relational graph payload into an interactive topology.
* **DiagnosticDashboard**: Scorecards displaying the 8 dimensions, overall Health Score, and list of specific rule violations.
* **RecommendationPanel**: Actionable cards mapping back to specific nodes in the Canvas.

### Backend Services & Storage Requirements
* **Storage:** Supabase Storage bucket (`workflow-artifacts`) storing raw PDFs/Images.
* **Pipeline Orchestrator:** FastAPI `BackgroundTasks` handling the multi-step Extraction -> Ontology -> Builder flow to prevent request timeouts.

---

## Part 8: Phased Execution Plan

The project will be delivered in the following sequential phases:

### Phase A: Upload & Extraction
* Configure Supabase Storage buckets.
* Implement `WorkflowUploadService` and FastAPI endpoints.
* Implement baseline OCR and standard text extraction tools.
* Wire up `BackgroundTasks` for asynchronous processing status tracking.

### Phase B: Graph Generation
* Implement `WorkflowGraphBuilder` schema and Pydantic validation.
* Deploy the PostgreSQL relational tables (`workflow_graphs`, `nodes`, `edges`).
* Implement the LLM `WorkflowOntologyMapper` prompt engineering to force raw data into the strict Node/Edge Types.
* Ensure frontend can fetch and render nodes via a simple React Flow layout.

### Phase C: APQC Classification
* Implement taxonomy database mapping.
* Integrate APQC classification prompt step in the ingestion pipeline.
* Update `workflow_graphs` with deterministic category/group assignment.

### Phase D: Workflow Diagnostics
* Implement the `DiagnosticRule` relational configuration table.
* Build the `WorkflowDiagnosticRunner` execution engine.
* Implement Phase 1 rules (e.g., Bottleneck via in-degree counting, cycle detection).
* Calculate and persist the 0-100 Health Score.

### Phase E: Recommendations
* Build the `WorkflowRecommendationEngine`.
* Map rule violations to actionable text insights.
* Expose recommendations via API and render in the frontend `RecommendationPanel`.

### Phase F: Forecasting Readiness (TimesFM)
* Ensure `workflow_nodes` and `workflow_edges` tables contain appropriate metadata fields (e.g., expected duration) to feed future time-series simulation models.
* Validate graph topological sort algorithms to ensure proper sequence delivery to the future TimesFM FastAPI microservice.
