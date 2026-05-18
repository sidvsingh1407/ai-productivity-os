from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from integration.router import router as integration_router

app = FastAPI(title="AI Productivity OS API")

app.include_router(integration_router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "ok", "version": "1.0.0"}
