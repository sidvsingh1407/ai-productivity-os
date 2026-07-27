import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from fastapi import HTTPException

from models.ai_system import AISystem
from ai_systems.schemas import AISystemCreate, AISystemUpdate, AISystemResponse, AISystemListResponse, CapabilityMapResponse
from data_intelligence.scoring import calculate_data_score
from financial.scoring import calculate_roi_score
from adoption.service import AdoptionRecordsService

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

    async def get_capability_map(self, db: AsyncSession, organization_id: uuid.UUID) -> List[CapabilityMapResponse]:
        stmt = (
            select(AISystem)
            .where(AISystem.organization_id == organization_id)
            .order_by(AISystem.created_at.desc())
        )
        result = await db.execute(stmt)
        systems = result.scalars().all()

        capability_map = []
        adoption_service = AdoptionRecordsService()

        # Optimize N+1: Fetch all adoption records for the organization once
        all_adoption_records = await adoption_service.list_records(
            db=db,
            organization_id=organization_id,
            limit=10000
        )
        # Group records by ai_system_id
        adoption_by_system = {}
        for record in all_adoption_records:
            if record.ai_system_id not in adoption_by_system:
                adoption_by_system[record.ai_system_id] = []
            adoption_by_system[record.ai_system_id].append(record)

        for system in systems:
            # 1. Adoption Score (Average of all records for this system)
            system_adoption_records = adoption_by_system.get(system.id, [])

            adoption_score = None
            if system_adoption_records:
                total_score = sum(record.adoption_score for record in system_adoption_records)
                adoption_score = total_score / len(system_adoption_records)

            # 2. Data Score
            # If all data intelligence fields are empty, override the calculator to return None
            data_types = system.data_types or []
            data_sources = system.data_sources or []
            data_destinations = system.data_destinations or []

            data_sensitivity = system.data_sensitivity
            data_freshness = system.data_freshness
            data_owner = system.data_owner
            data_accessibility = system.data_accessibility or []

            is_data_empty = (
                not data_types and
                not data_sources and
                not data_destinations and
                not data_sensitivity and
                not data_freshness and
                not data_owner and
                not data_accessibility
            )

            if is_data_empty:
                data_score = None
            else:
                data_score = calculate_data_score(system)

            # 3. ROI Score
            roi_data = calculate_roi_score(system)

            capability_map.append(
                CapabilityMapResponse(
                    id=system.id,
                    name=system.name,
                    ai_type=system.ai_type,
                    criticality=system.criticality,
                    lifecycle_status=system.lifecycle_status,
                    department=system.department,
                    owner=system.owner,

                    adoption_score=adoption_score,
                    data_score=data_score,
                    roi_score=roi_data.get("roi_score"),
                    roi_score_unavailable_reason=roi_data.get("roi_score_unavailable_reason"),
                    cost_is_partial=roi_data.get("cost_is_partial"),
                    cost_missing_components=roi_data.get("cost_missing_components"),

                    data_types=data_types,
                    data_sources=data_sources,
                    data_destinations=data_destinations
                )
            )

        return capability_map
