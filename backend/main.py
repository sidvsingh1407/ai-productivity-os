from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.config import settings

app = FastAPI(title="AI Productivity OS API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from backend.reports.router import router as reports_router

app.include_router(reports_router)

@app.get("/")
async def root():
    return {"status": "ok", "version": "1.0.0"}
