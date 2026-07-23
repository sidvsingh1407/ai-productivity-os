import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from models.engineering_record import EngineeringRecord
from engineering.schemas import EngineeringRecordCreate, EngineeringRecordUpdate, EngineeringRecordResponse, EngineeringRecordListResponse

class EngineeringRecordsService:
    def _calculate_score(self, record: EngineeringRecord) -> float:
        score = 0.0

        # Dedicated team
        if record.has_dedicated_ai_team:
            score += 25
        elif record.team_size and record.team_size > 0:
            score += 15

        # MLOps maturity
        if record.has_mlops_pipeline:
            score += 25

        # Tooling
        if record.monitoring_tooling and len(record.monitoring_tooling) > 0:
            score += 15

        # DevOps / Prompt Eng
        if record.has_dedicated_devops:
            score += 15
        elif record.devops_support_type and record.devops_support_type.lower() != 'not_specified':
            score += 5

        if record.has_dedicated_prompt_engineer:
            score += 10

        # Budget
        if record.ai_engineering_budget and float(record.ai_engineering_budget) > 0:
            score += 10

        return min(100.0, score)

    def _to_response(self, record: EngineeringRecord) -> EngineeringRecordResponse:
        score = self._calculate_score(record)
        return EngineeringRecordResponse(
            **{c.name: getattr(record, c.name) for c in record.__table__.columns},
            engineering_score=score
        )

    def _to_list_response(self, record: EngineeringRecord) -> EngineeringRecordListResponse:
        score = self._calculate_score(record)
        return EngineeringRecordListResponse(
            **{c.name: getattr(record, c.name) for c in record.__table__.columns},
            engineering_score=score
        )

    async def create_record(self, db: AsyncSession, organization_id: uuid.UUID, data: EngineeringRecordCreate) -> EngineeringRecordResponse:
        new_record = EngineeringRecord(
            organization_id=organization_id,
            **data.model_dump()
        )
        db.add(new_record)

        try:
            await db.commit()
            await db.refresh(new_record)
        except IntegrityError as e:
            await db.rollback()
            # Catching the unique constraint violation
            if "uix_org_engineering_record" in str(e) or "UNIQUE constraint failed" in str(e):
                raise HTTPException(
                    status_code=409,
                    detail="An engineering intelligence record already exists for this organization."
                )
            raise e

        return self._to_response(new_record)

    async def list_records(
        self,
        db: AsyncSession,
        organization_id: uuid.UUID,
        limit: int = 50,
        offset: int = 0
    ) -> List[EngineeringRecordListResponse]:

        stmt = (
            select(EngineeringRecord)
            .where(EngineeringRecord.organization_id == organization_id)
            .order_by(EngineeringRecord.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        result = await db.execute(stmt)
        records = result.scalars().all()
        return [self._to_list_response(r) for r in records]

    async def get_record(self, db: AsyncSession, organization_id: uuid.UUID, record_id: uuid.UUID) -> EngineeringRecordResponse:
        stmt = select(EngineeringRecord).where(
            EngineeringRecord.id == record_id,
            EngineeringRecord.organization_id == organization_id
        )
        result = await db.execute(stmt)
        record = result.scalar_one_or_none()

        if not record:
            raise HTTPException(status_code=404, detail="Engineering record not found")

        return self._to_response(record)

    async def update_record(self, db: AsyncSession, organization_id: uuid.UUID, record_id: uuid.UUID, data: EngineeringRecordUpdate) -> EngineeringRecordResponse:
        stmt = select(EngineeringRecord).where(
            EngineeringRecord.id == record_id,
            EngineeringRecord.organization_id == organization_id
        )
        result = await db.execute(stmt)
        record = result.scalar_one_or_none()

        if not record:
            raise HTTPException(status_code=404, detail="Engineering record not found")

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(record, key, value)

        await db.commit()
        await db.refresh(record)
        return self._to_response(record)

    async def delete_record(self, db: AsyncSession, organization_id: uuid.UUID, record_id: uuid.UUID):
        stmt = select(EngineeringRecord).where(
            EngineeringRecord.id == record_id,
            EngineeringRecord.organization_id == organization_id
        )
        result = await db.execute(stmt)
        record = result.scalar_one_or_none()

        if not record:
            raise HTTPException(status_code=404, detail="Engineering record not found")

        await db.delete(record)
        await db.commit()
        return {"status": "success"}
