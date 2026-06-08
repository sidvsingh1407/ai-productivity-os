# PDF Export Investigation Report

## Root Cause
The root cause of the PDF export failure is a schema mismatch between the application code and the database model.
Specifically, the `ExportJob` model in `backend/models/report.py` is missing the `audit_id` (and potentially `org_id`) columns, while multiple layers of the application (schemas, service layer, routers, and background tasks) assume these columns exist and actively query or write to them. Since the column doesn't exist on the SQLAlchemy model or in the database, trying to create or query an `ExportJob` using `audit_id` fails.

## Evidence

1. **Model Definition (`backend/models/report.py`)**:
   The `ExportJob` class only defines `id`, `user_id`, `job_type`, `status`, `result_path`, and `created_at`.

2. **Service Layer (`backend/reports/service.py`)**:
   The `request_pdf_export` function attempts to instantiate `ExportJob` with `org_id` and `audit_id`:
   ```python
   new_job = ExportJob(
       user_id=uuid.UUID(user_id),
       org_id=uuid.UUID(org_id),
       audit_id=uuid.UUID(audit_id),
       job_type=ExportJobType.pdf,
       status=ExportJobStatus.pending
   )
   ```

3. **Background Task (`backend/tasks/pdf_tasks.py`)**:
   The task tries to find the job using `ExportJob.audit_id`:
   ```python
   stmt_job = select(ExportJob).where(
       ExportJob.audit_id == audit_id,
       ExportJob.status == ExportJobStatus.pending
   )
   ```

4. **Schema Definition (`backend/reports/schemas.py`)**:
   `ExportJobResponse` strictly requires `org_id: UUID` and `audit_id: UUID`.

5. **Historical Migration (`backend/alembic/versions/3ff69d4ebaa6_initial_migration.py`)**:
   The initial Alembic migration strictly created `export_jobs` without `audit_id` or `org_id`:
   ```python
    op.create_table('export_jobs',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('user_id', sa.Uuid(), nullable=False),
    sa.Column('job_type', sa.Enum('pdf', 'csv', 'json', name='exportjobtype'), nullable=False),
    sa.Column('status', sa.Enum('pending', 'running', 'complete', 'failed', name='exportjobstatus'), nullable=False),
    sa.Column('result_path', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
   ```
   *Conclusion:* `audit_id` and `org_id` were never part of the initial schema. The model was never updated while the application code evolved to require these columns for auditing context.

## Complete Export Flow Diagram
1. User requests PDF via `POST /reports/export/{audit_id}` (`backend/reports/router.py`).
2. Router calls `service.request_pdf_export` with `audit_id`, `org_id`, `user_id`.
3. Service creates `ExportJob` (which fails due to missing fields).
4. Service triggers Celery task `generate_pdf_task.delay(audit_id, org_id)`.
5. Background task loads the Audit, creates the PDF, creates a `Report` record.
6. Background task queries `ExportJob` by `audit_id` (which fails due to missing `audit_id` column) to update its status to `complete`.
7. User polls `GET /reports/status/{job_id}` which returns job state and a download link once complete.

## Recommended Fix Option A
**Schema Change:** Add `audit_id` and `org_id` columns to the `ExportJob` model and create a corresponding Alembic migration.
* Modify `ExportJob` in `backend/models/report.py` to include `audit_id` (ForeignKey to `audits.id`) and `org_id` (ForeignKey to `organizations.id`).
* This aligns the database model with the current application logic.

## Recommended Fix Option B
**Code Change:** Refactor the application logic to remove the dependency on `audit_id` and `org_id` within the `ExportJob` context.
* Remove `audit_id` and `org_id` from `backend/reports/service.py` instantiation of `ExportJob`.
* Remove `audit_id` and `org_id` from `backend/reports/schemas.py`.
* In `backend/tasks/pdf_tasks.py`, instead of querying `ExportJob` by `audit_id`, pass the `job_id` directly to the background task (e.g., `generate_pdf_task.delay(audit_id, org_id, str(new_job.id))`) and update the job by its ID.

## Architectural Recommendation
**Option A** is the architecturally correct choice if `ExportJob` is intended to be a generic tracking table. However, since the system is exporting specific entities (like an `Audit`), adding context (`audit_id`, `org_id`) provides better traceability and allows for more robust authorization checks (e.g., ensuring a user can only view jobs for their org). Adding a polymorphic or generic reference (e.g., `entity_id`, `entity_type`) could also be considered, but adding `audit_id` is the simplest path to align with the current implementation.

Alternatively, if we prefer keeping `ExportJob` loosely coupled, **Option B** is better, passing the `job_id` down to the worker. But because `ExportJobResponse` exposes `audit_id` and `org_id` to the frontend, removing them might break frontend polling logic. Thus, **Option A** is strongly recommended to preserve frontend contracts.

## Migration Requirement
If **Option A** is chosen, a database migration **IS** required.
If **Option B** is chosen, a database migration is **NOT** required.

## Migration Impact
Adding `audit_id` and `org_id` to `ExportJob` is a low-impact migration. Existing `export_jobs` (if any exist) would need these columns to be `nullable=True` initially or have a default value, though since jobs are transient, it might be acceptable to clear old jobs or set them as nullable.

## Risk Level
**Low**. The task failure is isolated to the PDF export feature. Fixing it via schema update (Option A) has very little risk to other parts of the system, provided the migration handles existing records safely. Option B has a higher risk of breaking the frontend if it depends on `audit_id`/`org_id` in the polling response.

## Impact Analysis for Option A (Schema Change)

### Locations Involving ExportJob
1. **Creation**: `backend/reports/service.py:request_pdf_export` (creates job and sets `audit_id` and `org_id`).
2. **Reading**:
   * `backend/reports/service.py:get_export_job_status` (reads job by ID for status polling).
   * `backend/tasks/pdf_tasks.py:_generate_pdf_async` (reads job by `audit_id` and `status=pending` to mark it as complete).
3. **Updating**: `backend/tasks/pdf_tasks.py:_generate_pdf_async` (updates job status and result_path).
4. **API Schemas**: `backend/reports/schemas.py:ExportJobResponse` exposes `id`, `user_id`, `org_id`, `audit_id`, `job_type`, `status`, `result_path`, `download_url`, `created_at`.
5. **Frontend Consuming**:
   * `frontend/src/pages/AuditDetail.tsx` (calls `POST /reports/export/{id}` and polls `GET /reports/status/{job_id}`).
   * The frontend captures `data.job_id`. The frontend does not actively consume `audit_id` or `org_id` from the polling response.

### Migration Safety Assessment
* **Would adding nullable audit_id and org_id break existing code?**
  No. Existing code already attempts to write and read these fields. Adding them resolves the `AttributeError`/SQL errors currently occurring.
* **Would existing rows remain valid?**
  If existing rows have these fields as NULL (which is what `nullable=True` does), they would remain valid at the database level. Since they are already failing, there is no regression in behavior.
* **Would backfilling historical rows be required?**
  No. `ExportJob` rows are transient records used purely for tracking long-running exports. Old jobs do not strictly need backfilling for the system to remain healthy.
* **Would any API contracts change?**
  No, the API schemas already declare `audit_id` and `org_id`. This migration aligns the DB with the established API contract.
* **Would any frontend changes be required?**
  No, the frontend already hits the endpoints and expects the response shapes that the API schemas define.

### Rollback Strategy
If the migration causes unexpected issues, the rollback strategy is a standard Alembic downgrade:
`alembic downgrade -1`
This would drop the `audit_id` and `org_id` columns, reverting to the broken state.

### Final Recommendation
**Yes, Option A can be implemented as a backward-compatible migration with low deployment risk.**
It aligns the physical database schema with the established application data models and API contracts, without requiring changes to clients. It is the safest and most architecturally sound approach to fixing the issue.

## Final Decision
* Root cause confirmed.
* **Option A is approved** as the recommended fix.
* Option B is rejected unless new evidence emerges.

*Note: No code changes or migrations were implemented as part of this investigation. A separate implementation task will be created to execute Option A, verify PDF export end-to-end, and add tests.*