# Workflow Diagnostic Independence Architecture

## Overview
This document outlines the changes made to decouple the Workflow Diagnostic from the AI Audit, enabling it to act as a standalone product entry point.

## Dependency Analysis
- **Current State:**
  - The UI assumed `AI Audit -> Workflow Diagnostic` via the flow `Dashboard -> New Audit -> Audit Detail -> New Workflow`.
  - The `NewWorkflow.tsx` component was a dummy placeholder.
  - Integration logic was mistakenly pointing to `/integration` instead of `/integrations` in the frontend API calls.
  - The `Workflow` database table is inherently independent (contains `org_id`, `user_id`, `input_config`, and has no `audit_id` constraint). The `IntegrationResult` table links `Workflow` and `Audit` but only applies for the combined assessment.
- **Desired State:**
  - `Workflow Diagnostic` can be run completely independently via `Dashboard -> New Workflow -> Workflow Detail`.
  - The combined flow (Audit -> Workflow -> Integration) must still work.
- **Classified Dependencies:**
  - `Workflow` -> `Audit`: ACCIDENTAL in UX flow, NO dependency in database schema.
  - `IntegrationResult` -> `Workflow` and `Audit`: REQUIRED for the combined assessment.
  - `NewWorkflow` -> `auditId`: OPTIONAL (can be present for the combined flow).

## Files Changed
- `docs/architecture/WORKFLOW_DIAGNOSTIC_INDEPENDENCE.md`: Added.
- `frontend/src/App.tsx`: Added routing for `/workflows/new`, `/workflows/:id`, and `/integration/:id` (or `/integrations/:id`).
- `frontend/src/pages/NewWorkflow.tsx`: Implemented complete standalone form collecting Organization Type, Industry, Department, Workflow Category, Team Size, Current Tools Used, Workflow Description, and Current Challenges.
- `frontend/src/pages/Dashboard.tsx`: Added link to run independent Workflow Diagnostic.
- `frontend/src/pages/WorkflowDetail.tsx`: Fixed API endpoint (`/integration/run` -> `/integrations/run`).
- `frontend/src/pages/IntegrationResults.tsx`: Fixed router path and endpoint.

## Database Changes
No changes to the database schema were required.
- The `Workflow` table already exists without an `audit_id` constraint, making it fully independent.
- The `IntegrationResult` table appropriately requires both `audit_id` and `workflow_id` as it represents the combined intersection of an audit and a workflow. Making `audit_id` optional in `IntegrationResult` would corrupt its semantic purpose. Since standalone workflow results are stored directly in the `Workflow` table (and its child `Blueprints`), `IntegrationResult` is correctly relegated to only combined assessments.

## API Changes
No backend API schema or routing changes were required for this sequence.
- The `POST /workflows/` endpoint accepts a flexible `input_config: Dict[str, Any]`, which easily accommodates the new frontend form data without requiring backend migration risk.
- Fixed the frontend API client requests to match the correct backend endpoints (`/integrations` instead of `/integration`).

## Risks
- The open `input_config` dictionary on the backend defers validation to later processing steps, which should be hardened in Assessment Framework v1.
- Making the AI Pipeline depend on dynamic `input_config` values from the UI might produce unpredictable workflow mappings if the AI prompts rely on very specific phrasing.

## Testing Results
To be verified:
- Scenario A: User -> Dashboard -> Workflow Diagnostic -> Fill Form -> Submit -> Receive Results (WITHOUT AI Audit).
- Scenario B: User -> AI Audit -> Workflow Diagnostic -> Combined Flow Works.
- Scenario C: Existing AI Audit Flow remains unchanged.
