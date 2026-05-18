from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings

app = FastAPI(title="AI Productivity OS API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from admin.router import router as admin_router
from analytics.router import router as analytics_router
from billing.router import router as billing_router

app.include_router(admin_router, prefix="/admin", tags=["Admin"])
app.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
app.include_router(billing_router, prefix="/billing", tags=["Billing"])

@app.get("/")
async def root():
    return {"status": "ok", "version": "1.0.0"}
