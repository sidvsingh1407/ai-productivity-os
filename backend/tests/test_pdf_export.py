import asyncio
import uuid
import sys
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session_maker, Base, engine
from models.user import User
from models.organization import Organization, OrgRole
from models.audit import Audit
from models.report import ExportJob, ExportJobStatus, ExportJobType
from reports.service import request_pdf_export, get_export_job_status
from tasks.pdf_tasks import _generate_pdf_async

async def run_verification():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session_maker() as db:
        # Create user & org
        org_id = uuid.uuid4()
        user_id = uuid.uuid4()
        audit_id = uuid.uuid4()

        org = Organization(id=org_id, name="Test Org", slug="test-org")
        user = User(id=user_id, email="test@example.com", hashed_password="pw", full_name="Test User", is_active=True)
        audit = Audit(id=audit_id, org_id=org_id, user_id=user_id, total_score=85, rating="A", status="complete", form_response={"foo": "bar"})

        db.add(org)
        db.add(user)
        db.add(audit)
        await db.commit()

        # Verify: request_pdf_export() & ExportJob creation
        print("1. Testing request_pdf_export()...")
        # mocking generate_pdf_task.delay
        import tasks.pdf_tasks
        def fake_delay(a_id, o_id):
            print(f"Fake delay called with {a_id}, {o_id}")
        tasks.pdf_tasks.generate_pdf_task.delay = fake_delay

        job = await request_pdf_export(db, str(audit_id), str(org_id), str(user_id))
        print(f"Job created: id={job.id}, audit_id={job.audit_id}, org_id={job.org_id}")

        assert job.audit_id == audit_id
        assert job.org_id == org_id
        assert job.status == ExportJobStatus.pending

        job_id = str(job.id)

        # Verify: ExportJob lookup & get_export_job_status()
        print("2. Testing get_export_job_status()...")
        lookup_job = await get_export_job_status(db, job_id, str(user_id))
        assert lookup_job.id == job.id
        print("Lookup successful.")

        # Verify: PDF generation task
        print("3. Testing PDF generation task...")
        # running the async core of the celery task
        try:
            file_path = await _generate_pdf_async(str(audit_id), str(org_id))
            print(f"PDF generation completed: {file_path}")
        except Exception as e:
            print(f"PDF generation failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

        # Verify final status
        db.expunge_all() # ensure fresh fetch
        final_job = await get_export_job_status(db, job_id, str(user_id))
        assert final_job.status == ExportJobStatus.complete
        assert final_job.result_path is not None
        print(f"Final Job Status: {final_job.status}, Path: {final_job.result_path}")
        print("SUCCESS")

if __name__ == "__main__":
    asyncio.run(run_verification())
