import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi import HTTPException

from models.ai_system import AISystem
from ai_systems.schemas import AISystemCreate, AISystemUpdate

class AISystemsService:
    async def create_system(self, db: AsyncSession, organization_id: uuid.UUID, data: AISystemCreate) -> AISystem:
        new_system = AISystem(
            organization_id=organization_id,
            name=data.name,
            purpose=data.purpose,
            data_types=data.data_types,
            decision_making_role=data.decision_making_role,
            status=data.status
        )
        db.add(new_system)
        await db.commit()
        await db.refresh(new_system)
        return new_system

    async def list_systems(self, db: AsyncSession, organization_id: uuid.UUID, limit: int = 50, offset: int = 0) -> List[AISystem]:
        stmt = (
            select(AISystem)
            .where(AISystem.organization_id == organization_id)
            .order_by(AISystem.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_system(self, db: AsyncSession, organization_id: uuid.UUID, system_id: uuid.UUID) -> AISystem:
        stmt = select(AISystem).where(
            AISystem.id == system_id,
            AISystem.organization_id == organization_id
        )
        result = await db.execute(stmt)
        system = result.scalar_one_or_none()

        if not system:
            raise HTTPException(status_code=404, detail="AI System not found")

        return system

    async def update_system(self, db: AsyncSession, organization_id: uuid.UUID, system_id: uuid.UUID, data: AISystemUpdate) -> AISystem:
        system = await self.get_system(db, organization_id, system_id)

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(system, key, value)

        await db.commit()
        await db.refresh(system)
        return system

    async def delete_system(self, db: AsyncSession, organization_id: uuid.UUID, system_id: uuid.UUID):
        system = await self.get_system(db, organization_id, system_id)

        await db.delete(system)
        await db.commit()
        return {"status": "success"}
