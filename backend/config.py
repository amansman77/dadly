"""Configuration settings for Dadly backend."""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Supabase
    supabase_url: str = "https://test.supabase.co"
    supabase_anon_key: str = "test_anon_key"
    supabase_service_key: str = "test_service_key"
    
    # OpenAI
    openai_api_key: str = "sk-test123456789"
    
    # Qdrant
    qdrant_url: str = "https://test.qdrant.cloud"
    qdrant_api_key: str = "test_qdrant_key"
    
    # Cloudflare R2
    r2_endpoint: str = "https://test.r2.cloudflarestorage.com"
    r2_access_key: str = "test_access_key"
    r2_secret_key: str = "test_secret_key"
    r2_bucket: str = "dadly"
    
    # LangSmith
    langchain_tracing_v2: bool = True
    langchain_api_key: Optional[str] = ""
    langchain_project: str = "dadly"
    
    # App settings
    app_name: str = "Dadly"
    debug: bool = False
    
    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"  # Allow extra fields from .env


# Global settings instance
settings = Settings()

# Debug: Print LangSmith settings
print(f"LangSmith Tracing: {settings.langchain_tracing_v2}")
print(f"LangSmith API Key: {settings.langchain_api_key[:10] if settings.langchain_api_key else 'None'}...")
print(f"LangSmith Project: {settings.langchain_project}")
