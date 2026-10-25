import pytest
from httpx import ASGITransport, AsyncClient

from main import ALLOWED_ORIGINS, app


@pytest.mark.asyncio
async def test_cors_allowed_origin():
    origin = ALLOWED_ORIGINS[0]

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        # Normal response
        response = await client.get(
            "/health",
            headers={"Origin": origin},
        )
        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == origin

        # Preflight response
        response = await client.options(
            "/health",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code == 200
        assert response.headers.get("access-control-allow-origin") == origin

        # Error response must preserve CORS for an allowed origin
        response = await client.get(
            "/non-existent-endpoint",
            headers={"Origin": origin},
        )
        assert response.status_code == 404
        assert response.headers.get("access-control-allow-origin") == origin


@pytest.mark.asyncio
async def test_cors_disallowed_origin():
    origin = "http://evil-cors-origin.com"

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        # Normal response
        response = await client.get(
            "/health",
            headers={"Origin": origin},
        )
        assert response.status_code == 200
        assert "access-control-allow-origin" not in response.headers

        # Preflight response must not allow the origin
        response = await client.options(
            "/health",
            headers={
                "Origin": origin,
                "Access-Control-Request-Method": "GET",
            },
        )
        assert "access-control-allow-origin" not in response.headers

        # Error response must not add a wildcard or unauthorized origin
        response = await client.get(
            "/non-existent-endpoint",
            headers={"Origin": origin},
        )
        assert response.status_code == 404
        assert "access-control-allow-origin" not in response.headers


@pytest.mark.asyncio
async def test_cors_missing_origin():
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/health")

    assert response.status_code == 200
    assert "access-control-allow-origin" not in response.headers

