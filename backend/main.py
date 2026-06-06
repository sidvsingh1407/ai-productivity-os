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
    print("SYSTEM LOG: Database schema sync complete.", flush=True)
    yield

# Import all routers
from auth.router import router as auth_router  # noqa: E402
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
from config import settings  # noqa: E402
import re  # noqa: E402

app = FastAPI(title="AI Productivity OS", version="1.0.0", lifespan=lifespan)

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
        origin_allowed = re.fullmatch(
            settings.CORS_ALLOW_ORIGIN_REGEX, normalized_origin
        ) is not None

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
app.include_router(contact_router)
app.include_router(sample_router)
app.include_router(prompt_intelligence_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "AI Productivity OS Backend", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}
