from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

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

from config import settings
import re

# ADD CORS MIDDLEWARE (CRITICAL)
FRONTEND_URL = settings.FRONTEND_URL

def build_allowed_origins() -> list[str]:
    origins = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "https://ai-productivity-os-six.vercel.app"
    ]
    if FRONTEND_URL and FRONTEND_URL not in origins:
        origins.append(FRONTEND_URL)

    if settings.CORS_ALLOW_ORIGINS:
        for origin in settings.CORS_ALLOW_ORIGINS.split(","):
            origin = origin.strip()
            if origin and origin not in origins:
                origins.append(origin)
    return origins

ALLOWED_ORIGINS = build_allowed_origins()

def cors_error_headers(request: Request) -> dict[str, str]:
    origin = request.headers.get("origin")
    if not origin:
        return {}

    normalized_origin = origin.strip().rstrip("/")
    origin_allowed = normalized_origin in ALLOWED_ORIGINS

    if not origin_allowed and settings.CORS_ALLOW_ORIGIN_REGEX:
        origin_allowed = re.fullmatch(settings.CORS_ALLOW_ORIGIN_REGEX, normalized_origin) is not None

    if not origin_allowed:
        return {}

    return {
        "Access-Control-Allow-Origin": origin,
        "Access-Control-Allow-Credentials": "true",
        "Vary": "Origin",
    }

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger(__name__)

# ==================== EXCEPTION HANDLERS ====================

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail), "status_code": exc.status_code},
        headers=cors_error_headers(request)
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation Error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "status_code": 422},
        headers=cors_error_headers(request)
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception while processing request")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "status_code": 500},
        headers=cors_error_headers(request)
    )

# MOUNT ALL ROUTERS
app.include_router(auth_router)
app.include_router(admin_router, prefix="/admin")
app.include_router(audits_router, prefix="/audits")
app.include_router(analytics_router, prefix="/analytics")
app.include_router(workflows_router)
app.include_router(integration_router)
app.include_router(reports_router)
app.include_router(users_router)
app.include_router(organizations_router, prefix="/organizations")
app.include_router(billing_router, prefix="/billing")

@app.get("/")
async def root():
    return {"message": "AI Productivity OS Backend", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
