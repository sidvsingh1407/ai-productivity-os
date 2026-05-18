from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings
from backend.workflows.router import router as workflows_router

app = FastAPI(title="AI Productivity OS API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workflows_router)

@app.get("/")
async def root():
    return {"status": "ok", "version": "1.0.0"}
