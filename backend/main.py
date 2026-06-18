from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from database import engine, Base
import models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    print(
        "SYSTEM LOG: Scanning models and verifying tables on Supabase...",
        flush=True
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Run the seed to ensure temp dev user/org exist
    try:
        from seed_db import seed
        await seed()
        print("SYSTEM LOG: Development user seed complete.", flush=True)
    except Exception as e:
        logger.exception("SYSTEM LOG: Critical Seed Failure! The application may be missing required development user/org rows. Details: %s", e)

    print("SYSTEM LOG: Database schema sync complete.", flush=True)
    yield

# Import all routers
from admin.router import router as admin_router  # noqa: E402
from audits.router import router as audits_router  # noqa: E402
from analytics.router import router as analytics_router  # noqa: E402
from workflows.router import router as workflows_router  # noqa: E402
from integration.router import router as integration_router  # noqa: E402
from reports.router import router as reports_router  # noqa: E402
from users.router import router as users_router  # noqa: E402
from organizations.router import router as organizations_router  # noqa: E402
from billing.router import router as billing_router  # noqa: E402
from contact.router import router as contact_router  # noqa: E402
from sample.router import router as sample_router  # noqa: E402
from prompt_intelligence.router import router as prompt_intelligence_router # noqa: E402
from api_platform.router import router as api_platform_router
from api_platform.management_router import router as api_platform_management_router  # noqa: E402
from config import settings  # noqa: E402
import re  # noqa: E402

app = FastAPI(title="AI Productivity OS", version="1.0.0", lifespan=lifespan)

# ADD CORS MIDDLEWARE (CRITICAL)
# FRONTEND_URL exists to define the primary frontend origin for this environment.
# CORS_ALLOW_ORIGINS allows specifying a comma-separated list of additional allowed origins (e.g., preview deployments).
# Production domains should be configured by setting FRONTEND_URL (e.g. https://tarkax.vercel.app)
# and any additional valid domains via CORS_ALLOW_ORIGINS in the environment variables.
FRONTEND_URL = settings.FRONTEND_URL


def build_allowed_origins() -> list[str]:
    raw_origins = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]

    if FRONTEND_URL:
        raw_origins.append(FRONTEND_URL)

    if settings.CORS_ALLOW_ORIGINS:
        for origin in settings.CORS_ALLOW_ORIGINS.split(","):
            raw_origins.append(origin)

    # Normalize origins: strip whitespace, strip trailing slash, and remove duplicates
    normalized_origins = []
    for origin in raw_origins:
        cleaned_origin = origin.strip().rstrip("/")
        if cleaned_origin and cleaned_origin not in normalized_origins:
            normalized_origins.append(cleaned_origin)

    return normalized_origins


ALLOWED_ORIGINS = build_allowed_origins()

print("=== CORS CONFIGURATION ===", flush=True)
print(f"FRONTEND_URL: {FRONTEND_URL}", flush=True)
print(f"CORS_ALLOW_ORIGINS: {settings.CORS_ALLOW_ORIGINS}", flush=True)
print(f"CORS_ALLOW_ORIGIN_REGEX: {settings.CORS_ALLOW_ORIGIN_REGEX}", flush=True)
print(f"ALLOWED_ORIGINS: {ALLOWED_ORIGINS}", flush=True)


def cors_error_headers(request: Request) -> dict:
    origin = request.headers.get("origin")
    if not origin:
        return {"Access-Control-Allow-Origin": "*"}

    normalized_origin = origin.strip().rstrip("/")
    origin_allowed = normalized_origin in ALLOWED_ORIGINS

    if not origin_allowed and settings.CORS_ALLOW_ORIGIN_REGEX:
        origin_allowed = re.fullmatch(
            settings.CORS_ALLOW_ORIGIN_REGEX, normalized_origin
        ) is not None

    if not origin_allowed:
        return {"Access-Control-Allow-Origin": "*"}

    return {
        "Access-Control-Allow-Origin": normalized_origin,
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
async def http_exception_handler(request: Request, exc: StarletteHTTPException):  # noqa: E501
    logger.error(f"HTTP Exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": str(exc.detail), "status_code": exc.status_code},
        headers=cors_error_headers(request)
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):  # noqa: E501
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
# DANGER: Only for E2E Tests!
from tests.test_router import router as test_flow_router
app.include_router(test_flow_router)
app.include_router(admin_router, prefix="/admin")
app.include_router(audits_router, prefix="/audits")
app.include_router(analytics_router, prefix="/analytics")
app.include_router(workflows_router)
app.include_router(integration_router)
app.include_router(reports_router)
app.include_router(users_router)
app.include_router(organizations_router, prefix="/organizations")
app.include_router(billing_router, prefix="/billing")
app.include_router(contact_router)
app.include_router(sample_router)
app.include_router(prompt_intelligence_router, prefix="/api")
app.include_router(api_platform_router, prefix="/api/v1")
app.include_router(api_platform_management_router, prefix="/api/platform")


@app.get("/")
async def root():
    return {"message": "AI Productivity OS Backend", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
