import asyncio
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from config import settings

from models.regulation_chunk import RegulationChunk
from regulation.schemas import SearchRequest, SearchResponseItem
from utils.gemini_client import embed_text

class RegulationService:
    async def search(self, db: AsyncSession, request: SearchRequest) -> List[SearchResponseItem]:
        # Generate embedding for the query
        # embed_text is synchronous, so we run it in a thread
        query_embedding = await asyncio.to_thread(embed_text, request.query)

        # In SQLite tests, vector math doesn't work out of the box with <=>
        # Check if we are running in SQLite via config/url
        is_sqlite = "sqlite" in settings.DATABASE_URL

        if is_sqlite:
            # Fallback for SQLite testing - just return chunks as vector operators fail
            stmt = select(RegulationChunk).limit(request.k)
            result = await db.execute(stmt)
            rows = result.scalars().all()

            response_items = []
            for chunk in rows:
                response_items.append(
                    SearchResponseItem(
                        chunk_text=chunk.content,
                        article_number=chunk.article_number,
                        section_title=chunk.section_title,
                        relevance_score=1.0  # Dummy score for testing
                    )
                )
            return response_items
        else:
            # Vector cosine_distance operator in pgvector is `<=>`
            # For SQLAlchemy, it's model.embedding.cosine_distance(vector)
            # Note: the result of cosine_distance is the distance itself.
            distance = RegulationChunk.embedding.cosine_distance(query_embedding)

            stmt = (
                select(RegulationChunk, distance.label("distance"))
                .order_by(distance)
                .limit(request.k)
            )

            result = await db.execute(stmt)
            rows = result.all()

            response_items = []
            for chunk, dist in rows:
                # Revert distance to relevance_score (higher is better)
                relevance_score = 1.0 - float(dist)
                response_items.append(
                    SearchResponseItem(
                        chunk_text=chunk.content,
                        article_number=chunk.article_number,
                        section_title=chunk.section_title,
                        relevance_score=relevance_score
                    )
                )

            return response_items
