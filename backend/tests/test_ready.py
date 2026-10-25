import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db

client = TestClient(app)

def test_ready_success():
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}

class MockDBFailing:
    async def execute(self, *args, **kwargs):
        raise Exception("DB Connection Failed")

async def mock_get_db_fail():
    yield MockDBFailing()

def test_ready_failure():
    app.dependency_overrides[get_db] = mock_get_db_fail

    try:
        response = client.get("/ready")
        assert response.status_code == 503
        assert response.json() == {"status": "unavailable"}
        assert "Exception" not in response.text
    finally:
        app.dependency_overrides.pop(get_db, None)
