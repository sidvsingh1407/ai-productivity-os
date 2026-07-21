import uuid
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from models.adoption_record import AdoptionRecord
from adoption.schemas import AdoptionRecordCreate, AdoptionRecordUpdate

class AdoptionRecordsService:
    async def create_record(self, db: AsyncSession, organization_id: uuid.UUID, data: AdoptionRecordCreate) -> AdoptionRecord:
        new_record = AdoptionRecord(
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
            if "uix_ai_system_department" in str(e) or "UNIQUE constraint failed" in str(e):
                raise HTTPException(
                    status_code=409,
                    detail="An adoption record already exists for this AI System and department."
                )
            raise e

        return new_record

    async def list_records(
        self,
        db: AsyncSession,
        organization_id: uuid.UUID,
        ai_system_id: Optional[uuid.UUID] = None,
        department: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[AdoptionRecord]:

        stmt = (
            select(AdoptionRecord)
            .where(AdoptionRecord.organization_id == organization_id)
        )

        if ai_system_id:
            stmt = stmt.where(AdoptionRecord.ai_system_id == ai_system_id)

        if department:
            stmt = stmt.where(AdoptionRecord.department == department)

        stmt = stmt.order_by(AdoptionRecord.created_at.desc()).offset(offset).limit(limit)

        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_record(self, db: AsyncSession, organization_id: uuid.UUID, record_id: uuid.UUID) -> AdoptionRecord:
        stmt = select(AdoptionRecord).where(
            AdoptionRecord.id == record_id,
            AdoptionRecord.organization_id == organization_id
        )
        result = await db.execute(stmt)
        record = result.scalar_one_or_none()

        if not record:
            raise HTTPException(status_code=404, detail="Adoption record not found")

        return record

    async def update_record(self, db: AsyncSession, organization_id: uuid.UUID, record_id: uuid.UUID, data: AdoptionRecordUpdate) -> AdoptionRecord:
        record = await self.get_record(db, organization_id, record_id)

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(record, key, value)

        await db.commit()
        await db.refresh(record)
        return record

    async def delete_record(self, db: AsyncSession, organization_id: uuid.UUID, record_id: uuid.UUID):
        record = await self.get_record(db, organization_id, record_id)

        await db.delete(record)
        await db.commit()
        return {"status": "success"}
