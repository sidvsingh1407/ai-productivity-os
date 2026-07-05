import uuid
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from projects.models import Project, SavedPrompt
from billing.service import get_user_subscription_status
from fastapi import HTTPException

class ProjectsService:
    async def create_project(self, db: AsyncSession, user_id: uuid.UUID, name: str, description: str = None) -> Project:
        # Check limits
        stmt = select(func.count(Project.id)).where(Project.user_id == user_id)
        result = await db.execute(stmt)
        project_count = result.scalar()

        sub_status = get_user_subscription_status(user_id)
        if sub_status == "free" and project_count >= 3:
            raise HTTPException(
                status_code=402,
                detail={"detail": "limit_reached", "module": "projects", "limit": 3, "used": project_count}
            )

        new_project = Project(user_id=user_id, name=name, description=description)
        db.add(new_project)
        await db.commit()
        await db.refresh(new_project)
        return new_project

    async def list_projects(self, db: AsyncSession, user_id: uuid.UUID):
        # We need to return projects with their saved prompt counts
        stmt = (
            select(Project, func.count(SavedPrompt.id).label('saved_prompts_count'))
            .outerjoin(SavedPrompt, Project.id == SavedPrompt.project_id)
            .where(Project.user_id == user_id)
            .group_by(Project.id)
            .order_by(Project.created_at.desc())
        )
        result = await db.execute(stmt)

        projects_with_counts = []
        for row in result.all():
            project, count = row
            # We construct a dictionary that schema validation will handle
            proj_dict = {
                "id": project.id,
                "user_id": project.user_id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
                "saved_prompts_count": count
            }
            projects_with_counts.append(proj_dict)

        return projects_with_counts

    async def get_project(self, db: AsyncSession, user_id: uuid.UUID, project_id: uuid.UUID):
        # Get project
        stmt = select(Project).where(Project.id == project_id, Project.user_id == user_id)
        result = await db.execute(stmt)
        project = result.scalar_one_or_none()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        # Get saved prompts ordered by created_at desc
        prompts_stmt = select(SavedPrompt).where(SavedPrompt.project_id == project_id).order_by(SavedPrompt.created_at.desc())
        prompts_result = await db.execute(prompts_stmt)
        prompts = prompts_result.scalars().all()

        # Attach prompts manually for Pydantic to parse
        project.saved_prompts = prompts
        return project

    async def update_project(self, db: AsyncSession, user_id: uuid.UUID, project_id: uuid.UUID, name: str = None, description: str = None):
        stmt = select(Project).where(Project.id == project_id, Project.user_id == user_id)
        result = await db.execute(stmt)
        project = result.scalar_one_or_none()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        if name is not None:
            project.name = name
        if description is not None:
            project.description = description

        await db.commit()
        await db.refresh(project)
        return project

    async def delete_project(self, db: AsyncSession, user_id: uuid.UUID, project_id: uuid.UUID):
        stmt = select(Project).where(Project.id == project_id, Project.user_id == user_id)
        result = await db.execute(stmt)
        project = result.scalar_one_or_none()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        await db.delete(project)
        await db.commit()
        return {"status": "success"}

    async def save_prompt(self, db: AsyncSession, user_id: uuid.UUID, project_id: uuid.UUID, original_prompt: str, improved_prompt: str = None, title: str = None):
        # Verify project belongs to user
        stmt = select(Project).where(Project.id == project_id, Project.user_id == user_id)
        result = await db.execute(stmt)
        project = result.scalar_one_or_none()

        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        new_prompt = SavedPrompt(
            project_id=project_id,
            user_id=user_id,
            original_prompt=original_prompt,
            improved_prompt=improved_prompt,
            title=title
        )

        db.add(new_prompt)
        await db.commit()
        await db.refresh(new_prompt)
        return new_prompt

    async def delete_prompt(self, db: AsyncSession, user_id: uuid.UUID, project_id: uuid.UUID, prompt_id: uuid.UUID):
        stmt = select(SavedPrompt).where(
            SavedPrompt.id == prompt_id,
            SavedPrompt.project_id == project_id,
            SavedPrompt.user_id == user_id
        )
        result = await db.execute(stmt)
        prompt = result.scalar_one_or_none()

        if not prompt:
            raise HTTPException(status_code=404, detail="Prompt not found")

        await db.delete(prompt)
        await db.commit()
        return {"status": "success"}
