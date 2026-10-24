# Deployment Settings

This document outlines the expected configuration and deployment commands for the TarkaX application.

## Frontend
- **Build Command**: `npm run build`
- **Output Directory**: `dist` (default for Vite)
- **Environment Variables**:
  - `VITE_API_URL` (Required: backend API base URL)

## Backend
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port 8080` (as defined in `Dockerfile`)
- **Port**: `8080`
- **Health Checks**:
  - Liveness: `GET /health`
  - Readiness: `GET /ready` (Requires database connectivity)
- **Environment Variables**:
  - `DATABASE_URL` (Required: connection string)
  - `SECRET_KEY` (Required: for security features)
  - `ENVIRONMENT` (Optional: e.g. development, production)
  - `FRONTEND_URL` (Optional: for CORS)
  - `CORS_ALLOW_ORIGINS` (Optional: comma separated list of allowed domains)
  - `CORS_ALLOW_ORIGIN_REGEX` (Optional: regex for allowing origins)
  - `SUPABASE_URL` (Optional: for auth integration if used)
  - `SUPABASE_KEY` (Optional: for auth integration if used)
  - `REDIS_URL` (Optional)
  - `SENDGRID_API_KEY` (Optional)
  - `GEMINI_API_KEY1` (Optional)
  - `GEMINI_API_KEY2` (Optional)

## Database Configuration
The application expects `DATABASE_URL` to be provided in the environment. Continuous Integration (CI) test workflows use a test-only `pgvector/pgvector:pg16` database instance. **Never use production database credentials in CI.**
