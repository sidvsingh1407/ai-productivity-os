import pytest
from httpx import AsyncClient
from main import app
from models.user import User
import uuid
import pytest_asyncio
import tempfile
import docx

@pytest.fixture
def fake_user():
    return User(
        id=uuid.uuid4(),
        email="test@example.com",
        full_name="Test User",
        is_active=True,
        is_superadmin=False
    )

@pytest_asyncio.fixture
async def unauth_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest_asyncio.fixture
async def auth_client(fake_user):
    from dependencies import get_current_user
    app.dependency_overrides[get_current_user] = lambda: fake_user
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    app.dependency_overrides.pop(get_current_user, None)

@pytest.mark.asyncio
async def test_import_cv_unauthorized(unauth_client: AsyncClient):
    response = await unauth_client.post("/profile/import", files={"file": ("test.pdf", b"dummy content", "application/pdf")})
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_import_cv_invalid_format(auth_client: AsyncClient):
    response = await auth_client.post(
        "/profile/import",
        files={"file": ("test.txt", b"dummy content", "text/plain")}
    )
    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]

@pytest.mark.asyncio
async def test_import_cv_empty_file(auth_client: AsyncClient):
    response = await auth_client.post(
        "/profile/import",
        files={"file": ("test.pdf", b"", "application/pdf")}
    )
    assert response.status_code == 400
    assert "Uploaded file is empty" in response.json()["detail"]

@pytest.mark.asyncio
async def test_import_cv_oversized_file(auth_client: AsyncClient):
    large_content = b"a" * (10 * 1024 * 1024 + 10)
    response = await auth_client.post(
        "/profile/import",
        files={"file": ("test.pdf", large_content, "application/pdf")}
    )
    assert response.status_code == 400
    assert "size exceeds" in response.json()["detail"]

@pytest.mark.asyncio
async def test_import_cv_valid_docx(auth_client: AsyncClient, mocker):
    mocker.patch("profile.service.get_gemini_response", return_value='```json\n{"name": "John Doe", "email": "johndoe@example.com", "phone": null, "links": [], "experience": [], "education": [], "projects": [], "positions_of_responsibility": [], "volunteering": [], "certifications": [], "skills": [], "awards": []}\n```')

    # Create dummy docx file
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        doc = docx.Document()
        doc.add_paragraph('John Doe')
        doc.save(tmp.name)
        tmp_name = tmp.name

    with open(tmp_name, 'rb') as f:
        file_content = f.read()

    import os
    os.unlink(tmp_name)

    response = await auth_client.post(
        "/profile/import",
        files={"file": ("test.docx", file_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
