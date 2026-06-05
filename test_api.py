import asyncio
from httpx import AsyncClient, ASGITransport
import os
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["SECRET_KEY"] = "secret"
from main import app
from database import engine, Base

async def test():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/workflows/", json={
            "input_config": {
                "workflowDescription": "We manually extract data from pdfs, enter it into an excel spreadsheet, and then email it for manager approval. Sometimes the approval is delayed.",
                "currentChallenges": "It is very slow and there is a bottleneck at the manager approval step. Data is sometimes missing format.",
                "currentToolsUsed": "excel, email, pdf viewer",
                "teamSize": "10",
                "department": "Operations"
            }
        })
        print("Status code:", response.status_code)
        if response.status_code == 201:
            print("Intelligence key in response:", "intelligence" in response.json())
        else:
            print("Response:", response.text)

asyncio.run(test())
