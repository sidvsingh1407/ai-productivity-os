import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://user:password@localhost/aiproductivity"
    )
    
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    SENDGRID_API_KEY: str = os.getenv("SENDGRID_API_KEY", "")
    
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    CORS_ALLOW_ORIGINS: str = os.getenv("CORS_ALLOW_ORIGINS", "")
    CORS_ALLOW_ORIGIN_REGEX: str = os.getenv("CORS_ALLOW_ORIGIN_REGEX", "")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
