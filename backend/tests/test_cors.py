import pytest
from httpx import AsyncClient, ASGITransport
from main import app, ALLOWED_ORIGINS


@pytest.mark.asyncio
async def test_cors_allowed_origin():
    # Verify the origin is actually allowed
    test_origin = ALLOWED_ORIGINS[0]

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/health", headers={"origin": test_origin})
        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == \
            test_origin

        # Test error response
        response = await ac.get("/not-found", headers={"origin": test_origin})
        assert response.status_code == 404
        assert response.headers.get("access-control-allow-origin") == \
            test_origin


@pytest.mark.asyncio
async def test_cors_disallowed_origin():
    test_origin = "http://evil-cors-origin.com"

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/health", headers={"origin": test_origin})
        assert response.status_code == 200
        assert "access-control-allow-origin" not in response.headers

        # Test error response
        response = await ac.get("/not-found", headers={"origin": test_origin})
        assert response.status_code == 404
        assert "access-control-allow-origin" not in response.headers
