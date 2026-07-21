import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from database import get_db, async_session_maker
from dependencies import get_current_user, get_current_org
from models.user import User
from models.monitoring_plan import MonitoringPlan
from monitoring.schemas import MonitoringPlanResponse
from monitoring import service

router = APIRouter(tags=["Monitoring"])

@router.get("/", response_model=List[MonitoringPlanResponse])
async def list_monitoring_plans(
    skip: int = 0,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    org_id: uuid.UUID = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    """
    List monitoring plans for the current organization.
    """
    return await service.list_monitoring_plans(db, org_id, skip, limit)

@router.get("/{plan_id}", response_model=MonitoringPlanResponse)
async def get_monitoring_plan(
    plan_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    org_id: uuid.UUID = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    """
    Get a specific monitoring plan.
    """
    return await service.get_monitoring_plan(db, plan_id, org_id)

@router.post("/run-checks", status_code=202)
async def run_monitoring_checks(
    background_tasks: BackgroundTasks,
    # This endpoint is typically hit by an external cron/scheduler
):
    """
    Trigger the execution of due monitoring checks.
    """
    background_tasks.add_task(service.run_due_monitoring_checks, async_session_maker)
    return {"message": "Monitoring checks triggered successfully"}
