import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi import HTTPException

from models.ai_system import AISystem
from ai_systems.schemas import AISystemCreate, AISystemUpdate, AISystemResponse, AISystemListResponse
from data_intelligence.scoring import calculate_data_score
from financial.scoring import calculate_roi_score

class AISystemsService:
    def _to_response(self, system: AISystem) -> AISystemResponse:
        data_score = calculate_data_score(system)
        roi_data = calculate_roi_score(system)
        return AISystemResponse(
            **{c.name: getattr(system, c.name) for c in system.__table__.columns},
            data_score=data_score,
            roi_score=roi_data.get("roi_score"),
            roi_score_unavailable_reason=roi_data.get("roi_score_unavailable_reason"),
            cost_is_partial=roi_data.get("cost_is_partial"),
            cost_missing_components=roi_data.get("cost_missing_components")
        )

    def _to_list_response(self, system: AISystem) -> AISystemListResponse:
        data_score = calculate_data_score(system)
        roi_data = calculate_roi_score(system)
        return AISystemListResponse(
            **{c.name: getattr(system, c.name) for c in system.__table__.columns},
            data_score=data_score,
            roi_score=roi_data.get("roi_score"),
            roi_score_unavailable_reason=roi_data.get("roi_score_unavailable_reason"),
            cost_is_partial=roi_data.get("cost_is_partial"),
            cost_missing_components=roi_data.get("cost_missing_components")
        )

    async def create_system(self, db: AsyncSession, organization_id: uuid.UUID, data: AISystemCreate) -> AISystemResponse:
        new_system = AISystem(
            organization_id=organization_id,
            **data.model_dump()
        )
        db.add(new_system)
        await db.commit()
        await db.refresh(new_system)
        return self._to_response(new_system)

    async def list_systems(self, db: AsyncSession, organization_id: uuid.UUID, limit: int = 50, offset: int = 0) -> List[AISystemListResponse]:
        stmt = (
            select(AISystem)
            .where(AISystem.organization_id == organization_id)
            .order_by(AISystem.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = await db.execute(stmt)
        systems = result.scalars().all()
        return [self._to_list_response(s) for s in systems]

    async def get_system(self, db: AsyncSession, organization_id: uuid.UUID, system_id: uuid.UUID) -> AISystemResponse:
        stmt = select(AISystem).where(
            AISystem.id == system_id,
            AISystem.organization_id == organization_id
        )
        result = await db.execute(stmt)
        system = result.scalar_one_or_none()

        if not system:
            raise HTTPException(status_code=404, detail="AI System not found")

        return self._to_response(system)

    async def update_system(self, db: AsyncSession, organization_id: uuid.UUID, system_id: uuid.UUID, data: AISystemUpdate) -> AISystemResponse:
        stmt = select(AISystem).where(
            AISystem.id == system_id,
            AISystem.organization_id == organization_id
        )
        result = await db.execute(stmt)
        system = result.scalar_one_or_none()

        if not system:
            raise HTTPException(status_code=404, detail="AI System not found")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(system, key, value)

        await db.commit()
        await db.refresh(system)
        return self._to_response(system)

    async def delete_system(self, db: AsyncSession, organization_id: uuid.UUID, system_id: uuid.UUID):
        stmt = select(AISystem).where(
            AISystem.id == system_id,
            AISystem.organization_id == organization_id
        )
        result = await db.execute(stmt)
        system = result.scalar_one_or_none()

        if not system:
            raise HTTPException(status_code=404, detail="AI System not found")

        await db.delete(system)
        await db.commit()
        return {"status": "success"}
