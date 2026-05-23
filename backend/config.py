from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./test.db"
    SUPABASE_URL: str = ""
    SUPABASE_KEY: str = ""
    SECRET_KEY: str = "supersecret"
    REDIS_URL: str = "redis://localhost:6379/0"
    SENDGRID_API_KEY: str = ""
    FRONTEND_URL: str = "http://localhost:5173"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
