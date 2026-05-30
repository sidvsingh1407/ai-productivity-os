from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import all routers
from auth.router import router as auth_router
from admin.router import router as admin_router
from audits.router import router as audits_router
from analytics.router import router as analytics_router
from workflows.router import router as workflows_router
from integration.router import router as integration_router
from reports.router import router as reports_router
from users.router import router as users_router
from organizations.router import router as organizations_router
from billing.router import router as billing_router

app = FastAPI(title="AI Productivity OS", version="1.0.0")

# ADD CORS MIDDLEWARE (CRITICAL)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

allowed_origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

if ENVIRONMENT == "production":
    allowed_origins.append("https://ai-productivity-os-six.vercel.app")
    if FRONTEND_URL not in allowed_origins:
        allowed_origins.append(FRONTEND_URL)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MOUNT ALL ROUTERS
# Using prefixes only for routers that don't already define them internally
app.include_router(auth_router)                               # internal prefix: /auth
app.include_router(admin_router, prefix="/admin")             # missing prefix
app.include_router(audits_router, prefix="/audits")           # missing prefix
app.include_router(analytics_router, prefix="/analytics")     # missing prefix
app.include_router(workflows_router)                          # internal prefix: /workflows
app.include_router(integration_router)                        # internal prefix: /integrations
app.include_router(reports_router)                            # internal prefix: /reports
app.include_router(users_router)                              # internal prefix: /users
app.include_router(organizations_router)                      # internal prefix: /org
app.include_router(billing_router, prefix="/billing")         # missing prefix

@app.get("/")
async def root():
    return {"message": "AI Productivity OS Backend", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
