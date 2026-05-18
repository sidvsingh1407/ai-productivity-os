from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime

from config import settings

app = FastAPI(
    title="AI Productivity OS API",
    docs_url="/api/docs",
    redoc_url=None,
    openapi_url="/api/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now()}


@app.get("/")
async def root():
    return {"status": "ok", "version": "1.0.0"}
