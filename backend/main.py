from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from auth.router import router as auth_router
from users.router import router as users_router
from organizations.router import router as orgs_router
from workflows.router import router as workflows_router
from audits.router import router as audits_router
from integration.router import router as integration_router
from admin.router import router as admin_router
from analytics.router import router as analytics_router
from billing.router import router as billing_router
from reports.router import router as reports_router


app = FastAPI(title="AI Productivity OS API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-productivity-os-mu.vercel.app",
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(orgs_router)
app.include_router(workflows_router)
app.include_router(audits_router)
app.include_router(integration_router)
app.include_router(admin_router)
app.include_router(analytics_router)
app.include_router(billing_router)
app.include_router(reports_router)

@app.get("/")
async def root():
    return {"status": "ok", "version": "1.0.0"}
