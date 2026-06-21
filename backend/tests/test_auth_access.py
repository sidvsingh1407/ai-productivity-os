import pytest
from fastapi import FastAPI, Depends, HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

# Mock dependencies and minimal app for testing access control
from dependencies import get_current_user, get_current_org
from models.user import User
from models.organization import Organization
import uuid

app = FastAPI()

# Mock protected endpoint
@app.get("/protected-audits")
async def read_audits(current_user: User = Depends(get_current_user), current_org: Organization = Depends(get_current_org)):
    # Simulating backend repo query scoping
    return {"message": "Success", "org_id": str(current_org.id)}

client = TestClient(app)

def test_anonymous_user_rejected():
    """Verify that a request without an auth token is rejected."""
    response = client.get("/protected-audits")
    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"

def test_invalid_token_rejected():
    """Verify that a request with an invalid token is rejected."""
    response = client.get("/protected-audits", headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
    # Dependency returns "Could not validate credentials" for bad token
    assert "credentials" in response.json()["detail"].lower()

# Note: Full E2E testing of `get_current_user` and `get_current_org`
# with a real DB is beyond the scope of this isolated test, but we have
# validated the structural design.
