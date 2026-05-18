from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from auth.router import router as auth_router
from users.router import router as users_router
from organizations.router import router as org_router

app = FastAPI(title="AI Productivity OS API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(org_router)

@app.get("/")
async def root():
    return {"status": "ok", "version": "1.0.0"}
