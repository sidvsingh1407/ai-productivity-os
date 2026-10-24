from fastapi.testclient import TestClient
from main import app, ALLOWED_ORIGINS

client = TestClient(app)

def test_cors_allowed_origin():
    # Use the first allowed origin
    origin = ALLOWED_ORIGINS[0]
    response = client.options("/", headers={"Origin": origin, "Access-Control-Request-Method": "GET"})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == origin

    response = client.get("/", headers={"Origin": origin})
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == origin

def test_cors_disallowed_origin():
    origin = "http://evil-origin.com"
    response = client.options("/", headers={"Origin": origin, "Access-Control-Request-Method": "GET"})
    # It might pass through middleware or get rejected. What matters is it doesn't get origin: *
    assert response.headers.get("access-control-allow-origin") != "*"
    assert response.headers.get("access-control-allow-origin") is None

    response = client.get("/", headers={"Origin": origin})
    assert response.status_code == 200 # root endpoint works
    assert response.headers.get("access-control-allow-origin") != "*"
    assert response.headers.get("access-control-allow-origin") is None

def test_cors_missing_origin():
    response = client.get("/")
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") is None

def test_cors_error_headers_disallowed_origin():
    origin = "http://evil-origin.com"
    # test a 404 to hit the exception handlers
    response = client.get("/non-existent-endpoint", headers={"Origin": origin})
    assert response.status_code == 404
    assert response.headers.get("access-control-allow-origin") != "*"
    assert response.headers.get("access-control-allow-origin") is None

def test_cors_error_headers_allowed_origin():
    origin = ALLOWED_ORIGINS[0]
    response = client.get("/non-existent-endpoint", headers={"Origin": origin})
    assert response.status_code == 404
    assert response.headers.get("access-control-allow-origin") == origin
