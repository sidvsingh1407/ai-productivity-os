from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_current_user, get_db, get_current_org
from models.user import User
from models.organization import Organization
from projects.schemas import (
    ProjectCreate, ProjectUpdate, ProjectListResponse, ProjectDetailResponse,
    SavedPromptCreate, SavedPromptResponse
)
from projects.service import ProjectsService
import uuid

router = APIRouter(tags=["Projects"])
service = ProjectsService()

@router.post("/projects", response_model=ProjectDetailResponse)
async def create_project(
    request: ProjectCreate,
    current_user: User = Depends(get_current_user),
    current_org: Organization = Depends(get_current_org),
    db: AsyncSession = Depends(get_db)
):
    project = await service.create_project(db, current_user.id, current_org.id, request.name, request.description)
    return project

@router.get("/projects", response_model=List[ProjectListResponse])
async def list_projects(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.list_projects(db, current_user.id)

@router.get("/projects/{project_id}", response_model=ProjectDetailResponse)
async def get_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.get_project(db, current_user.id, project_id)

@router.put("/projects/{project_id}", response_model=ProjectDetailResponse)
async def update_project(
    project_id: uuid.UUID,
    request: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.update_project(db, current_user.id, project_id, request.name, request.description)

@router.delete("/projects/{project_id}")
async def delete_project(
    project_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_project(db, current_user.id, project_id)

@router.post("/projects/{project_id}/prompts", response_model=SavedPromptResponse)
async def save_prompt(
    project_id: uuid.UUID,
    request: SavedPromptCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.save_prompt(
        db, current_user.id, project_id,
        request.original_prompt, request.improved_prompt, request.title
    )

@router.delete("/projects/{project_id}/prompts/{prompt_id}")
async def delete_prompt(
    project_id: uuid.UUID,
    prompt_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await service.delete_prompt(db, current_user.id, project_id, prompt_id)
