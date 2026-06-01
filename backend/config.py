from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    
    SECRET_KEY: str
    
    REDIS_URL: str = "redis://localhost:6379/0"
    
    SENDGRID_API_KEY: str = ""
    
    FRONTEND_URL: str = "http://localhost:5173"
    
    ENVIRONMENT: str = "development"

    ALGORITHM: str = "HS256"
    CORS_ALLOW_ORIGINS: str = ""
    CORS_ALLOW_ORIGIN_REGEX: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
