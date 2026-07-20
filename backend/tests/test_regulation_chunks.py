import pytest
import os
import sqlalchemy as sa
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from models.regulation_chunk import RegulationChunk
from scripts.ingest_eu_ai_act import parse_markdown, ingest_eu_ai_act

# Mock Markdown fixture
MOCK_MARKDOWN = """## Chapter I — General Provisions

## Article 1 — Subject matter
1. The purpose of this Regulation is to improve the functioning of the internal market...
2. This Regulation lays down:
(a) harmonised rules...
(b) prohibitions...

## Article 2 — Scope
This Regulation applies to:
(a) providers placing on the market or putting into service AI systems...

## Annex I — Artificial Intelligence Techniques and Approaches
(a) Machine learning approaches, including supervised, unsupervised and reinforcement learning...
"""

def test_parse_markdown():
    """Test that the markdown parser correctly chunks headers and paragraphs."""
    chunks = parse_markdown(MOCK_MARKDOWN)

    # Expecting:
    # 1. Article 1(1)
    # 2. Article 1(2)
    # 3. Article 2
    # 4. Annex I
    assert len(chunks) == 4

    assert chunks[0]["article_number"] == "1(1)"
    assert chunks[0]["section_title"] == "Subject matter"
    assert "The purpose of this Regulation" in chunks[0]["content"]

    assert chunks[1]["article_number"] == "1(2)"
    assert chunks[1]["section_title"] == "Subject matter"
    assert "2. This Regulation lays down" in chunks[1]["content"]

    assert chunks[2]["article_number"] == "2"
    assert chunks[2]["section_title"] == "Scope"
    assert "This Regulation applies to" in chunks[2]["content"]

    assert chunks[3]["article_number"] == "Annex I"
    assert chunks[3]["section_title"] == "Artificial Intelligence Techniques and Approaches"
    assert "Machine learning approaches" in chunks[3]["content"]

@pytest_asyncio.fixture(autouse=True, scope="function")
async def setup_db():
    from database import engine, Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    from database import async_session_maker
    async with async_session_maker() as session:
        yield session

@pytest.mark.asyncio
async def test_ingest_eu_ai_act(mocker, db_session: AsyncSession):
    """Test the ingestion script logic with mocked db and embed_text."""

    # 1. Mock file reading and the file path
    mocker.patch("scripts.ingest_eu_ai_act.os.path.exists", return_value=True)
    mocker.patch("builtins.open", mocker.mock_open(read_data=MOCK_MARKDOWN))

    # 2. Mock embedding function to avoid API call
    mock_embedding = [0.1] * 768
    mocker.patch("scripts.ingest_eu_ai_act.embed_text", return_value=mock_embedding)

    # 3. Mock the async_session_maker to use the test session
    mock_session_maker = mocker.AsyncMock()
    mock_session_maker.__aenter__.return_value = db_session
    mocker.patch("scripts.ingest_eu_ai_act.async_session_maker", return_value=mock_session_maker)

    # 4. Run ingestion
    await ingest_eu_ai_act()

    # 5. Verify the DB
    result = await db_session.execute(sa.select(RegulationChunk))
    db_chunks = result.scalars().all()

    assert len(db_chunks) == 4
    assert db_chunks[0].source == "eu_ai_act"
    # Depending on DB dialect (sqlite vs postgres), the embedding list structure can differ slightly when queried,
    # but we can just check if it's not None.
    assert db_chunks[0].embedding is not None

    # 6. Test Idempotency (run again)
    await ingest_eu_ai_act()
    result_again = await db_session.execute(sa.select(RegulationChunk))
    db_chunks_again = result_again.scalars().all()

    # Should still be 4 chunks because the previous ones are deleted
    assert len(db_chunks_again) == 4
