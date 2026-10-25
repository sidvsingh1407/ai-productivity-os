import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from main import app, READY_DB_TIMEOUT_SECONDS


@pytest.mark.asyncio
async def test_health():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_ready_success(mocker):
    # Mock out _verify_schema_and_migrations to avoid attempting to validate in-memory db tables vs full app models
    mocker.patch("main._verify_schema_and_migrations", return_value=None)

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/ready")
        assert response.status_code == 200
        assert response.json() == {"status": "ready"}

@pytest.mark.asyncio
async def test_ready_missing_tables(mocker):
    mocker.patch(
        "main._verify_schema_and_migrations", side_effect=Exception("Missing required tables")
    )
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/ready")
        assert response.status_code == 503
        assert response.json() == {"status": "unavailable"}

@pytest.mark.asyncio
async def test_ready_migration_drift(mocker):
    mocker.patch(
        "main._verify_schema_and_migrations", side_effect=Exception("Alembic migration drift detected")
    )
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/ready")
        assert response.status_code == 503
        assert response.json() == {"status": "unavailable"}


@pytest.mark.asyncio
async def test_ready_db_failure(mocker):
    mocker.patch(
        "main._check_db_ready", side_effect=Exception("DB connection failed")
    )
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/ready")
        assert response.status_code == 503
        assert response.json() == {"status": "unavailable"}


@pytest.mark.asyncio
async def test_ready_db_timeout(mocker):
    async def slow_connect():
        await asyncio.sleep(READY_DB_TIMEOUT_SECONDS + 1)

    mocker.patch("main._check_db_ready", side_effect=slow_connect)
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/ready")
        assert response.status_code == 503
        assert response.json() == {"status": "unavailable"}
