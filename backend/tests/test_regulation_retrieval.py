import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from main import app
from config import settings
from models.user import User
from models.organization import Organization
from models.regulation_chunk import RegulationChunk

from tests.test_ai_systems import setup_db, db_session, user, organization

def get_auth_headers(user: User):
    to_encode = {"sub": str(user.id)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"Authorization": f"Bearer {encoded_jwt}"}

@pytest.fixture
async def sample_regulation_chunks(db_session: AsyncSession):
    chunks = [
        RegulationChunk(
            source="eu_ai_act",
            article_number="1(1)",
            section_title="Subject matter",
            content="The purpose of this Regulation is to improve the functioning of the internal market...",
            embedding=[0.1] * 768
        ),
        RegulationChunk(
            source="eu_ai_act",
            article_number="1(2)",
            section_title="Subject matter",
            content="This Regulation lays down: (a) harmonised rules for the placing on the market...",
            embedding=[0.2] * 768
        ),
        RegulationChunk(
            source="eu_ai_act",
            article_number="2",
            section_title="Scope",
            content="This Regulation applies to: (a) providers placing on the market or putting into service...",
            embedding=[0.3] * 768
        )
    ]
    db_session.add_all(chunks)
    await db_session.commit()
    return chunks

@pytest.mark.asyncio
async def test_regulation_search_success(db_session: AsyncSession, user: User, organization: Organization, sample_regulation_chunks, monkeypatch):
    headers = get_auth_headers(user)

    # We must await the fixture here in pytest_asyncio sometimes if it doesn't auto-resolve
    if hasattr(sample_regulation_chunks, '__await__'):
        await sample_regulation_chunks

    monkeypatch.setattr("regulation.service.embed_text", lambda text: [0.15] * 768)

    payload = {
        "query": "What is the purpose of this regulation?",
        "k": 2
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/regulation/search", json=payload, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2

        # Verify structure
        for item in data:
            assert "chunk_text" in item
            assert "article_number" in item
            assert "section_title" in item
            assert "relevance_score" in item
            assert isinstance(item["relevance_score"], float)
            assert item["relevance_score"] <= 1.0  # Cosine similarity bounds

@pytest.mark.asyncio
async def test_regulation_search_respects_k(db_session: AsyncSession, user: User, organization: Organization, sample_regulation_chunks, monkeypatch):
    headers = get_auth_headers(user)

    if hasattr(sample_regulation_chunks, '__await__'):
        await sample_regulation_chunks

    monkeypatch.setattr("regulation.service.embed_text", lambda text: [0.15] * 768)

    payload = {
        "query": "Search query",
        "k": 1
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/regulation/search", json=payload, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

@pytest.mark.asyncio
async def test_regulation_search_no_matches(db_session: AsyncSession, user: User, organization: Organization, monkeypatch):
    headers = get_auth_headers(user)

    monkeypatch.setattr("regulation.service.embed_text", lambda text: [0.9] * 768)

    payload = {
        "query": "Something completely irrelevant",
        "k": 5
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        response = await client.post("/regulation/search", json=payload, headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 0
